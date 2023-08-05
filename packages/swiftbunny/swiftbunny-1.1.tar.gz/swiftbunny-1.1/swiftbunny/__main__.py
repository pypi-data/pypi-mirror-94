#!/usr/bin/env python3
# swiftbunny -- CLI/daemon to help with log archiving to OpenStack Swift
# Copyright (C) 2020  Walter Doekes, OSSO B.V.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO: rotate a key!
# TODO: record file size and begin complaining when we near the 10GB mark
# (we compress.. likely 10x, but we want to stay below 4GB for swift..)
import fcntl
import json
import logging
import logging.config
import math
import os
import re
import signal
import sys

from datetime import datetime, timedelta
from subprocess import check_call

from keystone_light import (
    Cloud, DirectConfig, ChunkIteratorIOBaseWrapper, SwiftContainerGetPipe)

from .osso_ez_gpg import DeflatePipe, InflatePipe, DecryptPipe, EncryptPipe
try:
    from .osso_ez_rmq import BaseConsumer, rmq_uri
except ImportError as e:
    class _ErrCls:  # noqa
        _errstr = 'laoding RabbitMQ dependencies failed: {}'.format(e)
        def __init__(self, *args, **kwargs):  # noqa
            raise ImportError(self._errstr)
    BaseConsumer = rmq_uri = _ErrCls  # noqa

log = logging.getLogger('swiftbunny')


def _periodic_reporter(signum, frame):
    signal.alarm(60)  # reinit
    assert signum == signal.SIGALRM, signum
    if hasattr(periodic_reporter, 'report'):
        periodic_reporter.report()


def setup_periodic_report():
    global periodic_reporter
    periodic_reporter = None
    signal.signal(signal.SIGALRM, _periodic_reporter)
    signal.alarm(60)


def setup_log(debug=False):
    logconfig = {
        'version': 1,
        'formatters': {
            'full': {
                'format': '%(asctime)-15s: %(levelname)s: %(message)s'}},
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler', 'formatter': 'full'}},
        'loggers': {
            '': {'handlers': ['console'], 'level': 'WARNING'},
            'swiftbunny': {
                'handlers': ['console'], 'level': 'INFO',
                'propagate': False}},
    }
    logging.config.dictConfig(logconfig)
    if debug:
        log.setLevel('DEBUG')


class StateError(ValueError):
    pass


def ExclusiveFile(fp):
    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as e:
        raise StateError(
            'Could not get exclusive access on {!r}; '
            'running two processes?'.format(fp.name)) from e
    return fp


def datetime_truncate(dt, delta_sec):
    assert delta_sec in (1, 10, 60, 1800, 3600, 86400), delta_sec
    dt = dt.replace(microsecond=0)
    off = (dt.hour * 3600 + dt.minute * 60 + dt.second)
    return dt - timedelta(seconds=(off % delta_sec))


class BaseMessage:
    __slots__ = ('bin', 'dict', 'time')
    STRICT = True

    @classmethod
    def parse_flatmessage_time(cls, line):
        "Parse only the time"
        tm = line[0:27].decode('ascii')  # "2020-05-19T11:00:00.000000Z"
        return datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.%fZ')

    @classmethod
    def parse_flatmessage(cls, line):
        assert line[26:30] == b'Z: {' and line[-2:] == b'}\n', line
        tm = line[0:27].decode('ascii')  # "2020-05-19T11:00:00.000000Z"
        body = line[29:-1]
        return cls(
            bin=body,
            dict=json.loads(body.decode('utf-8')),
            time=datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.%fZ'))

    @classmethod
    def parse_binary(cls, body):
        try:
            tbody = body.decode('utf-8')
        except UnicodeDecodeError:
            log.exception('while parsing {}'.format(body))
            if cls.STRICT:
                raise
            obody = {'binaryblob': str(body)}  # 'b"some binary blob"'
            timestamp = datetime.utcnow()
        else:
            try:
                obody = json.loads(tbody)
            except ValueError:
                log.exception('while parsing {}'.format(body))
                if cls.STRICT:
                    raise
                obody = {'textblob': tbody}  # "some readable blob"
                timestamp = datetime.utcnow()
            else:
                try:
                    timestamp = cls.parse_timestamp(obody)
                except ValueError:
                    log.exception('while parsing {}'.format(body))
                    if cls.STRICT:
                        raise
                    timestamp = datetime.utcnow()

        return cls(bin=body, dict=obody, time=timestamp)

    @staticmethod
    def parse_timestamp(dict):
        raise NotImplementedError()

    def __init__(self, bin, dict, time):
        self.bin = bin
        self.dict = dict
        self.time = time  # agnostic, in UTC

    def as_flat_message(self):
        """
        A flat message looks like: 2006-01-02T15:04:05.000000Z: {"json":"dict"}
        """
        tm = self.time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        js = json.dumps(
            # Set esure_ascii to False, so allow readable UTF-8 output.
            # (We might as well allow all 8-bits.)
            # Set sort_keys to True to for consistent output.
            self.dict, skipkeys=False, ensure_ascii=False,
            check_circular=False, separators=(', ', ': '),
            sort_keys=True)
        return '{time}: {json}\n'.format(time=tm, json=js)

    def __str__(self):
        return self.as_flat_message()[0:-1]  # without LF


class FluentdMessage(BaseMessage):
    """
    Regular JSON log message that went through fluentd first
    """
    @staticmethod
    def parse_timestamp(dict):
        try:
            tm = dict['fluentd_time']
        except KeyError:
            raise ValueError('missing fluentd_time')
        # [15:48 CEST] <jordi> "fluentd_time":"2020-04-21 13:45:56,947"
        # I.e. fluentd_time timestamps are in UTC. Good.
        return datetime.strptime(tm, '%Y-%m-%d %H:%M:%S,%f')


class GraylogElasticMessage(BaseMessage):
    """
    Graylog message exported from ElasticSearch

    {
      "_index": "acceptance_applicationlogs_140",
      "_type": "message",
      "_id": "c41ccafa-5fcc-4cc8-8873-833dd89b7471",
      "_score": 1,
      "_source": {
        "modificationSource": "SSRC",
        "source": "some-machine.acceptance.svc.cluster.local",
        "gl2_source_input": "656970686935696f3273eeb5",
        ...
        "timestamp": "2019-12-25 12:36:32.043"
      }
    }
    """
    @staticmethod
    def parse_timestamp(dict):
        try:
            tm = dict['_source']['timestamp']
        except KeyError:
            raise ValueError('missing _source.timestamp')
        # NOTE: Unsure what the time is. Assume it's already UTC.
        return datetime.strptime(tm, '%Y-%m-%d %H:%M:%S.%f')


class FlatMessages:
    def __init__(self, expected_period, fallback_min=None):
        """
        Take a date and a period; accept messages which are marginally earlier

        fallback_min = 202-05-19 12:00:00
        period = 1800

        Adding of messages between [11:30, 12:30] (exclusive) is allowed.
        For messages _after_, can_add() will return false.
        For messages _before_, you'll get an exception.

        We only use fallback_min if there is no data in the scratchpad. If
        there already was data, we'll prefer the min time from there.
        """
        # Allow setting SWIFTBUNNY_FLUSH and SWIFTBUNNY_FSYNC envvars for
        # flush/sync to disk.
        self._swiftbunny_fsync = (
            os.environ.get('SWIFTBUNNY_FSYNC', '') not in ('', '0'))
        self._swiftbunny_flush = self._swiftbunny_fsync or (
            os.environ.get('SWIFTBUNNY_FLUSH', '') not in ('', '0'))

        # path_to_scratchpad = os.path.dirname(__file__)
        # scratchpad_filename = os.path.join(path_to_scratchpad, 'scratchpad')
        path_to_scratchpad = settings.SCRATCHPAD_DIR
        scratchpad_filename = os.path.join(
            path_to_scratchpad, settings.SCRATCHPAD_NAME)

        self._fp = ExclusiveFile(open(scratchpad_filename, 'a+b'))
        self._count = 0

        # The expected dates will be used when naming the resultant file:
        # we'll expect all messages to land withing that period.
        self._expected_min = self._expected_max = None
        self._expected_period = expected_period  # seconds: 60, 3600, 86400

        # These dates are what we actually have. This can include some messages
        # from outside the period if they were late to arrive in the queue.
        self._date_min = None
        self._date_max = None

        # Load old data from scratchpad, and set fp to tail. If there are
        # already items in there, we'll use those to define our period.
        self._load_old_data()

        # If we loaded 0 data, then use the fallback_min as period start.
        if self._expected_min is None:
            assert datetime_truncate(fallback_min, expected_period) == (
                fallback_min)
            self._expected_min = fallback_min  # rounded datetime
            self._expected_max = (
                fallback_min + timedelta(seconds=expected_period))

    def _load_old_data(self):
        """
        Load old data, update dates and counts, and point the end of the
        scratchpad
        """
        # Is the file 0-sized?
        if self._fp.seek(0, os.SEEK_END) != 0:
            log.info(
                'Scratchpad at %s contained %s bytes; checking',
                self._fp.name, self._fp.tell())

            # At this point, we should check dates. We may be looking at
            # very-old records, and we might need to change date selection
            # behaviour..?
            self._fp.seek(0, os.SEEK_SET)
            it = iter(self._fp)

            if self._expected_min is None:
                line = next(it)
                time = BaseMessage.parse_flatmessage_time(line)
                self._expected_min = datetime_truncate(
                    time, self._expected_period)
                self._expected_max = (
                    self._expected_min +
                    timedelta(seconds=self._expected_period))
                self._count += 1
                self._up_date(time)

            for line in it:
                time = BaseMessage.parse_flatmessage_time(line)

                self._count += 1
                self._up_date(time)
                if ((self._expected_min - self._date_min).total_seconds()
                        > self._expected_period):
                    # If the min_time is larger than the period we may be
                    # overstretching things.
                    raise StateError(
                        'More than period min_time in scratch pad; please fix')

            # Should be at end now.
            self._fp.seek(0, os.SEEK_END)
            log.info('Scratchpad caught up')

    def _up_date(self, time):
        "Update _date_min and _date_max"
        if self._date_min is None:
            assert self._date_max is None
            self._date_min = self._date_max = time
        elif time > self._date_max:
            # We may want to relax this restriction..
            assert time < self._expected_max, (self._expected_max, time)
            self._date_max = time
        elif time < self._date_min:
            self._date_min = time

    def create_for_next_period(self):
        """
        Create a new FlatMessages for the period after this period

        Call this after you've called discard_file() or eject_file() on this
        one.
        """
        # expected_max == expected_min + expected_period
        return self.__class__(self._expected_period, self._expected_max)

    def report(self):
        """
        This can be called periodically by a SIGALRM handler
        """
        from time import time

        new_t = time()

        if hasattr(self, '_last_t'):
            time_d = new_t - self._last_t
            count_d = self._count - self._last_c
            c_per_s = count_d / time_d

            if c_per_s > 1:
                speed = '{:.1f}/s'.format(c_per_s)
            elif (c_per_s * 60) > 1:
                speed = '{:.1f}/m'.format(c_per_s * 60)
            else:
                speed = '{:.1f}/h'.format(c_per_s * 3600)
        else:
            speed = '???/s'

        log.debug(
            'Populating %s+%s: %d messages (%s)', self._expected_min,
            self._expected_period, self._count, speed)

        self._last_c = self._count
        self._last_t = new_t

    def count(self):
        return self._count

    def discard_file(self):
        """
        Discard file if it was empty

        You cannot add() any messages after ejecting.
        """
        log.warning('%s: discarding file', self.formatted_times())
        assert self._fp, 'already discarded/ejected'
        assert not self._count, 'trying to discard a non-empty file?'
        fp, self._fp = self._fp, None  # detach our fp
        fp.flush()
        assert fp.tell() == 0, fp.tell()
        fp.close()
        os.unlink(fp.name)

    def eject_file(self):
        """
        Eject file from FlatMessage for someone else to process

        You cannot add() any messages after ejecting.
        """
        log.debug('%s: ejecting file', self.formatted_times())
        assert self._fp, 'already discarded/ejected'
        assert self._count, 'trying to get an empty file?'
        fp, self._fp = self._fp, None  # detach our fp
        fp.flush()
        return fp

    def can_add(self, message):
        """
        Can we add more, or is it time to rotate
        """
        return message.time < self._expected_max

    def add(self, message):
        """
        Add message to scratch pad
        """
        self._up_date(message.time)  # before write() because of assertions
        self._fp.write(message.as_flat_message().encode('utf-8'))

        if self._swiftbunny_flush:
            # If you want to see what's going on, it's nice if stuff is flushed
            # to the OS immediately.
            self._fp.flush()
            if self._swiftbunny_fsync:
                # If you want extra safety against crashes, ask the OS to flush
                # _every_ _new_ _line_ to disk. This might slow things down (a
                # lot).
                os.fsync(self._fp.fileno())

        self._count += 1

    def formatted_times(self):
        """
        E.g. '2020-05-21T00:00:00Z+86400-13x55'

        2020-05-21 00:00:00 UTC -> start time
        +86400 -> planned/max period (1 day in file)
        -13 -> one or more messages at most 13 secs _before_ start date
        55 -> message count in file
        """
        # We expect most of the times to be within the start and start+period.
        # But we may get some older (or newer?) messages.
        start = self._expected_min.strftime('%Y-%m-%dT%H:%M:%SZ')
        plus_time = math.ceil(
            (max(self._date_max or self._expected_max, self._expected_max) -
                self._expected_min)
            .total_seconds())
        min_time = math.ceil(
            (self._expected_min - (
                min(self._date_min or self._expected_min, self._expected_min)))
            .total_seconds())
        return '{start}+{plus}-{min}x{count}'.format(
            start=start, count=self._count, plus=plus_time, min=min_time)

    def start_time(self):
        return self._expected_min


class FlatMessagesUploader:
    def __init__(self, flatmessages):
        self._time = flatmessages.start_time()
        self._remote_name = self._make_remote_name(
            basename=settings.SWIFT_FILE,
            infix=flatmessages.formatted_times(),  # XXX: use start_time?
            keyid=settings.PASSPHRASE_ID)
        self._passphrase = settings.PASSPHRASE_VALUE
        self._source = flatmessages.eject_file()
        self._source.seek(0, os.SEEK_END)
        self._source_len = self._source.tell()

    def get_swift_container(self, time):
        if '%' in settings.SWIFT_CONTAINER:
            # logbunny-test-%Y => logbunny-test-2020
            container_name = time.strftime(settings.SWIFT_CONTAINER)
        else:
            container_name = settings.SWIFT_CONTAINER

        try:
            container = self._get_swift_container[container_name]
        except (AttributeError, KeyError):
            if not hasattr(self, '_get_swift_container'):
                self._get_swift_container = {}

            config = DirectConfig(settings.KEYSTONE_URI)
            project = Cloud(config).get_current_project()
            assert project.get_fullname() == settings.SWIFT_PROJECT, (
                project.get_fullname())

            swift = project.get_swift()
            container = swift.get_container(container_name)
            container.ensure_exists()
            self._get_swift_container[container_name] = container

        return container

    def _make_remote_name(self, basename, infix, keyid, ext='.qz1.gpg'):
        """
        <basename>/2020/05/19/<basename>_<infix>_<keyid>.qz1.gpg

        Where infix is expected to start with YYYY-MM-DD.
        (See FlatMessages.formatted_times())
        """
        yy, mm, rest = infix.split('-', 2)
        dd, rest = rest.split('T', 1)
        filename = '{base}/{yy}/{mm}/{dd}/{base}_{infix}_{key}{ext}'.format(
            base=basename, yy=yy, mm=mm, dd=dd, infix=infix,
            key=keyid, ext=ext)
        return filename

    def upload(self):
        """
        Upload the file to Swift, in encrypted form
        """
        container = self.get_swift_container(self._time)
        log.info(
            'Uploading %s byte source to %s: %s', self._source_len,
            container.name, self._remote_name)

        self._source.seek(0, os.SEEK_SET)  # rewind
        with DeflatePipe(self._source) as pipe1, \
                EncryptPipe(pipe1.stdout, password=self._passphrase) as pipe2:
            container.put(
                self._remote_name, ChunkIteratorIOBaseWrapper(pipe2.stdout))
            pipe2.communicate()
            pipe1.communicate()
            log.info(
                'Uploaded %s byte source to %s: %s', self._source_len,
                container.name, self._remote_name)

    def verify_upload(self):
        """
        Download uploaded file to a temp location, and compare to source
        """
        container = self.get_swift_container(self._time)
        log.info(
            'Downloading %s from %s for verification', self._remote_name,
            container.name)

        self._source.seek(0, os.SEEK_END)
        size = self._source.tell()
        self._source.seek(0, os.SEEK_SET)  # rewind
        with SwiftContainerGetPipe(container, self._remote_name) as pipe1, \
                DecryptPipe(
                    pipe1.stdout, password=self._passphrase) as pipe2, \
                InflatePipe(pipe2.stdout) as pipe3:
            try:
                # Compare block by block. Assume that the inflate-pipe
                # does not send stuff to stderr (which we'd need to
                # read so it doesn't block).
                pos = 0
                buf = buf2 = True
                while buf and buf2:
                    buf = self._source.read(8192)   # ends with b''
                    buf2 = pipe3.stdout.read(8192)  # also ends with b''
                    if buf != buf2:
                        break  # break before incrementing pos
                    pos += len(buf)  # +8192, +8192, +123, +0
                if buf != buf2:
                    log.error(
                        'Verification of %s failed after byte %d (+8192): '
                        'expected %r got %r',
                        self._remote_name, pos, buf, buf2)
                    pipe3.kill()  # this should kill off all pipes
                    raise StateError('Verification failed')
                assert pos == size, 'source {}, remote {}'.format(size, pos)
            finally:
                # Cleanup
                # FIXME: when pipe3.kill() is called, this will still
                # yield garbage and do an AssertionError in
                # communicate(). Perhaps check for is_killed there?
                pipe3.communicate()
                pipe2.communicate()
                pipe1.communicate()

            log.info(
                'Verified file %s (%d decoded bytes) on %s',
                self._remote_name, size, container.name)

    def free(self):
        """
        You must free the source when done
        """
        self._source.close()
        os.unlink(self._source.name)


class RmqFluentdConsumer(BaseConsumer):
    def __init__(self, uri):
        self._rmqc = rmq_uri(uri)
        log.debug('Setting up RabbitMQ connection from URI: %s', self._rmqc)
        super().__init__()

        # We'll create the flatmessages as soon as the first message arrives.
        # Then we'll know which time period we're dealing with.
        self._flatmessages = None

    def run_for_as_long_as_necessary(self):
        """
        The RabbitMQ queue consumer will run forever
        """
        while True:
            log.info('Starting consumer')
            self.run()
            log.info('Stopped consumer')

    def on_message(self, channel, deliver, properties, body):
        global periodic_reporter

        m = FluentdMessage.parse_binary(body)

        if self._flatmessages is None:
            # If there never was any, create the first one, based on first
            # message we get.
            start_time = datetime_truncate(m.time, settings.PERIOD)
            self._flatmessages = FlatMessages(settings.PERIOD, start_time)

            # "Reporter, reporting for reporting!"
            periodic_reporter = self._flatmessages

            # The above may have taken its time and toll. Disconnect and return
            # so we bail out of the run(). And let the caller restart.
            # (while True: consumer.run())
            try:
                self.close()
            except Exception:
                log.exception('FlatMessages init took too long?')
                raise
            return

        if not self._flatmessages.can_add(m):
            periodic_reporter = None  # pause status reports

            if self._flatmessages.count() == 0:
                self._flatmessages.discard_file()
            else:
                uploader = FlatMessagesUploader(self._flatmessages)
                uploader.upload()
                uploader.verify_upload()  # NOTE: not strictly necessary..
                uploader.free()
                uploader = None

            self._flatmessages = self._flatmessages.create_for_next_period()
            periodic_reporter = self._flatmessages

            # The above may have taken its time and toll. Disconnect and return
            # so we bail out of the run(). And let the caller restart.
            # (while True: consumer.run())
            try:
                self.close()
            except Exception:
                log.exception('FlatMessages push took too long?')
                raise
            return

        self._flatmessages.add(m)
        channel.basic_ack(deliver.delivery_tag)


class _ElasticSearchJsonDumpProducer:
    def __init__(self, uri):
        assert uri.startswith('elasticjs://'), uri

        file_re = uri[len('elasticjs://'):]
        file_path, file_re = file_re.rsplit('/', 1)
        file_re = re.compile(file_re, re.DOTALL)

        files = [i for i in os.listdir(file_path) if file_re.fullmatch(i)]
        convert = (lambda text: int(text) if text.isdigit() else text.lower())
        sort_re = (re.compile(r'([0-9]+)', re.DOTALL))
        files.sort(key=(lambda x: tuple(convert(i) for i in sort_re.split(x))))

        self._files = [os.path.join(file_path, i) for i in files]

    def run_for_as_long_as_necessary(self):
        """
        The elastic search dump consumer will run until all files are consumed
        """
        log.info('Starting consumer')

        for filename in self._files:
            # Here we expect that files contain exactly one day.
            # But the values are not sorted, so we'll do a double pass.
            sorted_filename = self._create_sorted_dump(filename)

            # Now they're sorted. Go go go.
            log.info('Opening file %s', sorted_filename)
            with open(sorted_filename, 'rb') as fp:
                for line in fp:
                    # XXX: ouch! we already parsed these! don't do so again :(
                    self.on_message(line[29:])
            os.unlink(sorted_filename)

            # Also, we're done with the source. Remove?
            # XXX: we should do this automatically; but we need to be sure that
            # we're not in the middle of a file that's still being written to
            log.warn('Renaming: %s', filename)
            os.rename(filename, '{}.processed'.format(filename))

        # TODO: flush the last one!
        # TEMP: disabled because we always expect one more dump; and we don't
        # want to upload the head of the next dump yet.
#        self.flush()

        log.info('Stopped consumer')

    def _create_sorted_dump(self, filename):
        log.info('Opening file %s; for sorting', filename)
        with open(filename, 'rb') as fp:
            # #filename = '/tmp/{}'.format(os.path.basename(filename)) # ?
            with open(filename + '.unsorted', 'wb') as outfp:
                it = iter(fp)
                try:
                    line = next(it)
                except StopIteration:
                    # 0 byte file? Ok sure.
                    count, wrong_date = 0, 0
                else:
                    m = GraylogElasticMessage.parse_binary(line)
                    last_date = m.time.date()
                    outfp.write(m.as_flat_message().encode('utf-8'))
                    count, wrong_date = 1, 0
                    for line in it:
                        m = GraylogElasticMessage.parse_binary(line)
                        if last_date != m.time.date():
                            wrong_date += 1
                        count += 1
                        outfp.write(m.as_flat_message().encode('utf-8'))

        # To make matters worse: this wrong_date only says something about the
        # input. If there was an issue and we're fed old files, this part will
        # not detect that they're old. And the consumer -- which may be
        # expecting newer logs -- will not know that these are "old files". The
        # system is designed to cope with incidental old records after all.
        log.info('Found %d lines, %d with different date', count, wrong_date)
        log.info('Sorting file %s.unsorted', filename)
        assert '\\' not in filename and "'" not in filename, filename
        check_call(
            # We must have a wrapper around qlzip1(1) in /usr/local/bin
            # for sort(1) that accepts 'qlzip1 -d' to decompress.
            # (The compression may be needed on non-compressing
            # filesystems when we're dealing with large files to sort.)
            "sort --compress-program=/usr/local/bin/qlzip1 "
            "'{f}.unsorted' >'{f}.sorted'".format(f=filename),
            shell=True)
        os.unlink('{f}.unsorted'.format(f=filename))

        return '{f}.sorted'.format(f=filename)


class ElasticSearchJsonDumpConsumer(_ElasticSearchJsonDumpProducer):
    def __init__(self, uri):
        super().__init__(uri)
        self._flatmessages = None

    def on_message(self, body):
        global periodic_reporter

        m = GraylogElasticMessage.parse_binary(body)

        if self._flatmessages is None:
            # If there never was any, create the first one, based on first
            # message we get.
            start_time = datetime_truncate(m.time, settings.PERIOD)
            self._flatmessages = FlatMessages(settings.PERIOD, start_time)

            # "Reporter, reporting for reporting!"
            periodic_reporter = self._flatmessages

        if not self._flatmessages.can_add(m):
            self.flush()

        self._flatmessages.add(m)

    def flush(self):
        global periodic_reporter
        periodic_reporter = None  # pause status reports

        if self._flatmessages.count() == 0:
            self._flatmessages.discard_file()
        else:
            uploader = FlatMessagesUploader(self._flatmessages)
            uploader.upload()
            uploader.verify_upload()  # NOTE: not strictly necessary..
            uploader.free()
            uploader = None

        self._flatmessages = self._flatmessages.create_for_next_period()
        periodic_reporter = self._flatmessages


def get_consumer(uri):
    if uri.startswith('elasticjs://'):
        return ElasticSearchJsonDumpConsumer
    elif uri.startswith('rmq://'):
        return RmqFluentdConsumer
    else:
        assert False, uri


def main():
    global settings

    import configparser
    import functools

    assert len(sys.argv) in (4, 5), sys.argv
    assert sys.argv[1] == '-c'  # --config-file
    config_file = sys.argv[2]   # FILENAME
    section_name = sys.argv[3]  # [ini_section]
    config = configparser.ConfigParser(interpolation=None)
    with open(config_file, 'r') as fp:
        config.readfp(fp)
    config_get = functools.partial(config.get, section_name)

    class Settings:
        CONSUME_URI = config_get('CONSUME_URI')
        SCRATCHPAD_DIR = config_get(
            'SCRATCHPAD_DIR', fallback='/var/spool/swiftbunny')
        SCRATCHPAD_NAME = config_get('SCRATCHPAD_NAME', fallback=section_name)

        KEYSTONE_URI = config_get('KEYSTONE_URI')
        SWIFT_PROJECT = config_get('SWIFT_PROJECT')
        SWIFT_CONTAINER = config_get('SWIFT_CONTAINER')
        SWIFT_FILE = config_get('SWIFT_FILE', fallback=section_name)
        PERIOD = int(config_get('PERIOD') or 3600)

        PASSPHRASE_ID = config_get('PASSPHRASE_ID')
        PASSPHRASE_VALUE = config_get('PASSPHRASE_VALUE')

    # Global settings..
    settings = Settings()

    setup_log(debug=(sys.argv[4:5] == ['--debug']))
    setup_periodic_report()

    consumer_class = get_consumer(settings.CONSUME_URI)
    consumer = consumer_class(settings.CONSUME_URI)
    consumer.run_for_as_long_as_necessary()


if __name__ == '__main__':
    main()

# vim: set ts=8 sw=4 sts=4 et ai:
