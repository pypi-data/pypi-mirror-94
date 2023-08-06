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
import subprocess
import tempfile
import unittest
from collections import namedtuple
from pathlib import Path

from setuptools import Distribution

import yaml
from setup_headers.command import LicenseHeaderCommand, run_command
from setup_headers.process import DEFAULT_CONFIG_FILE, readlines

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

    def testCommandInstantiation(self):
        command = LicenseHeaderCommand(Distribution())
        self.assertEqual(command.config, DEFAULT_CONFIG_FILE)
        self.assertFalse(command.dry_run)
        command.dry_run = True
        self.assertTrue(command.dry_run)
        command.finalize_options()
        command.run()

    def testSetupDryRun(self):
        self.maxDiff = None
        cmd = ("python setup.py adjust_license_headers --dry-run "
               "--config test/data/config/02_config.yaml")
        process = subprocess.run(cmd.split(),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        self.assertEqual(process.stderr, "")
        self.assertEqual(0, process.returncode)
        print(process.stdout)
