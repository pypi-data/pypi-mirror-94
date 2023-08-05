# SwiftBunny -- CLI/daemon to help with log archiving to OpenStack Swift
# Copyright (C) 2020,2021  Walter Doekes, OSSO B.V.
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
from distutils.core import setup
from os.path import dirname, join


if __name__ == '__main__':
    long_descriptions = []
    with open(join(dirname(__file__), 'README.rst')) as file:
        long_descriptions.append(file.read())
    version = '1.1'

    setup(
        name='swiftbunny',
        version=version,
        data_files=[
            ('share/doc/swiftbunny', [
                'LICENSE', 'README.rst', 'requirements.txt']),
            ('share/swiftbunny', ['swiftbunny@.service', 'swiftbunny.ini'])],
        entry_points={'console_scripts': [
            'swiftbunny = swiftbunny.__main__:main']},
        packages=['swiftbunny'],
        description='CLI/daemon to help with log archiving to OpenStack Swift',
        long_description=('\n\n\n'.join(long_descriptions)),
        author='Walter Doekes, OSSO B.V.',
        author_email='wjdoekes+swiftbunny@osso.nl',
        url='https://github.com/ossobv/swiftbunny',
        license='GPLv3+',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: No Input/Output (Daemon)',
            'Intended Audience :: System Administrators',
            ('License :: OSI Approved :: GNU General Public License v3 '
             'or later (GPLv3+)'),
            'Programming Language :: Python :: 3',
            'Topic :: System :: Archiving',
            'Topic :: System :: Logging',
            'Topic :: Utilities',
        ],
        install_requires=[
            'keystone-light>=1.0',
        ],
    )

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
