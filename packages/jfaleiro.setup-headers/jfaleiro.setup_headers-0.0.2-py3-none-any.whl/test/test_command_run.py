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
import os
import shutil
import tempfile
import unittest
from collections import namedtuple
from pathlib import Path

import yaml
from setup_headers.command import run_command
from setup_headers.process import readlines

_TEST_DATA_DIR = Path('test')/'data'

Command = namedtuple('Command', 'config dry_run')


class Test(unittest.TestCase):
    def testCommandRun(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            config_file = os.path.join(temp_dir, 'config.yaml')
            command = Command(config=config_file,
                              dry_run=False)
            shutil.copy("test/data/02_file.txt", temp_dir)
            config = dict(header=str(_TEST_DATA_DIR / "02_header.txt"),
                          prefixes=[dict(prefix='#',
                                         globs=[
                                             os.path.join(temp_dir, "**/*.txt")
                                         ])])
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

            run_command(command)
            self.assertEqual(
                readlines(os.path.join(temp_dir,  "02_file.txt")),
                readlines("test/data/02_expected.txt")
            )

    def testCommandDryRun(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            config_file = os.path.join(temp_dir, 'config.yaml')
            command = Command(config=config_file,
                              dry_run=True)
            shutil.copy("test/data/02_file.txt", temp_dir)
            config = dict(header=str(_TEST_DATA_DIR / "02_header.txt"),
                          prefixes=[dict(prefix='#',
                                         globs=[
                                             os.path.join(temp_dir, "**/*.txt")
                                         ])])
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

            run_command(command)
            self.assertEqual(
                readlines(os.path.join(temp_dir,  "02_file.txt")),
                readlines("test/data/02_file.txt")
            )
