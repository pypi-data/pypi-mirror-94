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
import tempfile
import unittest
from pathlib import Path

import yaml
from setup_headers.process import (DEFAULT_HEADER,
                                   ConfigurationValidationError, read_config)

_TEST_DATA_DIR = Path('test')/'data'/'config'


class Test(unittest.TestCase):
    def testReadConfig(self):
        self.assertEqual(
            read_config(_TEST_DATA_DIR / '01_config.yaml'),
            {'header': 'HEADER',
             'excludes': [],
             'prefixes': [
                 {'globs': ['setup_headers/**/*.py',
                            'test/**/*.py',
                            '.devcontainer/Dockerfile',
                            'Makefile'],
                  'prefix': '#'},
                 {'globs': ['*.yml', '*.yaml'],
                  'prefix': '##'},
                 {'globs': [
                     '.devcontainer/devcontainer.json'],
                     'prefix': '//'}]})

    def testDoublePrefix(self):
        with self.assertRaises(ConfigurationValidationError) as e:
            read_config(_TEST_DATA_DIR /
                        '01_config_double_prefix.yaml')
        self.assertEqual(e.exception.args,
                         ({'prefixes': [
                             "prefix {'#'} defined more than once"]},))

    def testDoubleGlob(self):
        with self.assertRaises(ConfigurationValidationError) as e:
            read_config(_TEST_DATA_DIR /
                        '01_config_double_glob.yaml')
        self.assertEqual(e.exception.args,
                         ({'prefixes': [
                          "glob {'Makefile'} defined more than once"]},))

    def testHeaderDoesNotExist(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            filename = os.path.join(temp_dir, "sample.yaml")
            with open(filename, 'w') as outfile:
                yaml.dump(dict(header='DOES_NOT_EXIST'), outfile,
                          default_flow_style=False)
                with self.assertRaises(ConfigurationValidationError) as e:
                    read_config(filename)
                self.assertEqual(e.exception.args,
                                 ({'header': [
                                     'header file "DOES_NOT_EXIST" is '
                                     'not a file or does not exist']},))

    def testHeaderDefault(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            filename = os.path.join(temp_dir, "sample.yaml")
            with open(filename, 'w') as outfile:
                yaml.dump(dict(), outfile, default_flow_style=False)
            result = read_config(filename)
            self.assertTrue("header" in result)
            self.assertEqual(result["header"], DEFAULT_HEADER)

    def testPrefixesDefault(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            filename = os.path.join(temp_dir, "sample.yaml")
            with open(filename, 'w') as outfile:
                yaml.dump(dict(), outfile, default_flow_style=False)
            result = read_config(filename)
            self.assertTrue("prefixes" in result)
            self.assertEqual(result["prefixes"], list())

    def testExcludesDefault(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            filename = os.path.join(temp_dir, "sample.yaml")
            with open(filename, 'w') as outfile:
                yaml.dump(dict(), outfile, default_flow_style=False)
            result = read_config(filename)
            self.assertTrue("excludes" in result)
            self.assertEqual(result["excludes"], list())


if __name__ == "__main__":
    unittest.main()
