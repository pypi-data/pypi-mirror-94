#!/usr/bin/env python
#
#     setup_headers - Sets a standard header in all source files
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr. == j@falei.ro
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse

from .process import DEFAULT_CONFIG_FILE, process_all, process_file


def main(params=None):

    class Parser(argparse.ArgumentParser):
        def parse_args(self, args=None, namespace=None):
            namespace = super().parse_args(args, namespace)
            with namespace.config:
                namespace.config = namespace.config.name
                files = set()
                for file in namespace.files:
                    with file:
                        files.add(file.name)
                namespace.files = files
            return namespace

    parser = Parser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config',
                        default=DEFAULT_CONFIG_FILE,
                        type=argparse.FileType('r'),
                        help='name of the YAML config file')
    parser.add_argument('--dry-run',
                        default=False,
                        action='store_true',
                        help="don't apply any changes")
    parser.add_argument('--prefix-mandatory',
                        default=False,
                        action='store_true',
                        help="failure if file is not associated to a prefix")
    parser.add_argument('files',
                        type=argparse.FileType('r'),
                        nargs='*',
                        help=("process only files in the list"))
    args = parser.parse_args(params)
    if len(args.files) == 0:
        process_all(args)
    else:
        process_file(args)


if __name__ == '__main__':  # pragma: no cover
    exit(main())
