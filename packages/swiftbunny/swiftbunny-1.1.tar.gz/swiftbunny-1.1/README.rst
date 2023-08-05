SwiftBunny :: CLI/daemon to help with log archiving to OpenStack Swift
======================================================================

Reads RabbitMQ, reads Graylog+ElasticSearch JSON dumps.

Writes daily/hourly logs files to OpenStack Swift.

Encrypts data on the fly using *qpress* (``.qz1``) and *GnuPG*.

*Why?* Organised long term storage of logs.


Output file format
------------------

Time is duplicated in the file, as the datetime is taken from the JSON object.
The compression will take care of excess size::

    2020-01-25T00:00:12.217000Z: {"some": "json", "dict": "..."}
    2020-01-25T00:00:12.496000Z: {"another": "json", "object": "..."}
    ...

Target file names will look like::

    example-swift-container-2020/example.rabbit.queue/2020/05/31/
      example.rabbit-queue_2020-05-25T00:00:00Z+3600-0x72272_keyid.qz1.gpg

Which means:

* the target container is ``example-swift-container-2020``;

* the source queue is ``example.rabbit.queue``;

* the first message is after ``2020-05-25``, at ``00:00:00`` (UTC);

* the last message is before that time ``+3600`` (i.e. one hour later);

* there are *no* late message (``-0``);

* the file contains ``72272`` lines (records).

* ``keyid`` may describe which node this was produced on, and a short
  identifier which symmetric gpg key was used.


So, if you're looking for old records, you can:

* find all files in the right period (also check nearby files with
  ``-N``-times);

* fetch, decrypt and decompress the files;

* scan the lines by the consistently formatted timestamps.


TODO
----

* Add commands, so we can do 'ls' and 'get' and 'post' on the archived files.
  (Use argparse.)

* Add sample ini-file.

* Fix suffix (split node-X and keyname).

* Add Immutable middleware to Swift so we can make it harder to
  accidentally delete stored logs.

* Don't forget about chmod 600 in swiftbunny.ini and chmod 700 on
  /var/spool/swiftbunny.
