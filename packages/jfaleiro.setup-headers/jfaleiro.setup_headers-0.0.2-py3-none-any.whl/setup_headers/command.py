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

from setuptools import Command

from .process import DEFAULT_CONFIG_FILE, process_all


class LicenseHeaderCommand(Command):
    """
    adds a standard copyright header to source files
    """
    description = __doc__.strip()
    user_options = [
        ('config=', 'c', ('YAML configuration file '
                          f'(default={DEFAULT_CONFIG_FILE})')),
        ('dry-run', 'd', 'dry run (optional)'),
    ]

    def initialize_options(self):
        self.config = DEFAULT_CONFIG_FILE
        self.dry_run = False

    def finalize_options(self):
        assert self.config is not None, 'configuration file is required'
        assert self.dry_run is not None, 'dry run flag is required'

    def run(self):
        run_command(self)


def run_command(args):
    process_all(args)
