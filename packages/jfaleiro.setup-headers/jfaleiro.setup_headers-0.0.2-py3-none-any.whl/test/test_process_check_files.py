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
from setup_headers.process import (FileParsingValidationError, chain,
                                   check_files, read_config, scan_globs)

_TEST_DATA_DIR = Path('test')/'data'/'config'


class Test(unittest.TestCase):

    def testConfigResolveNoFiles(self):
        config = chain(
            _TEST_DATA_DIR / "03_config_no_files.yaml",
            read_config,
            scan_globs)

        with self.assertRaises(FileParsingValidationError) as e:
            check_files(config)
        self.assertEqual(e.exception.args, (
            {
                'header': [
                    {
                        'prefixes': [
                            'no files for glob test/data/**/zz_e*.txt'
                        ]
                    }
                ]
            },)
        )

    def testConfigResolveNoFilesAfterExclude(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            filename = os.path.join(temp_dir, "sample.yaml")
            with open(filename, 'w') as outfile:
                config = dict(
                    excludes=[
                        r"^test/data/01_.*\.txt",
                        r"^test/data/02_.*\.txt"
                    ],
                    prefixes=[
                        {"prefix": "#",
                         "globs": [
                             "test/data/01_file.txt"
                         ]},
                        {"prefix": "##",
                         "globs": [
                             "test/data/02_file.txt"
                         ]}
                    ]
                )
                yaml.dump(config, outfile,
                          default_flow_style=False)
            with self.assertRaises(FileParsingValidationError) as e:
                chain(
                    filename,
                    read_config,
                    scan_globs,
                    check_files
                )
            print(e.exception.args)
            self.assertEqual(e.exception.args, (
                {'header': [
                    {'prefixes': [
                        'no files for glob test/data/02_file.txt after '
                        'excludes',
                        'no files for glob test/data/01_file.txt after '
                        'excludes']}]},)
            )

    def testConfigResolveDuplicateFile(self):
        config = chain(
            _TEST_DATA_DIR / "03_config_duplicate_file.yaml",
            read_config,
            scan_globs)
        print(config)

        with self.assertRaises(FileParsingValidationError) as e:
            check_files(config)
        self.assertEqual(e.exception.args, (
            {
                'header': [
                    {'prefixes': [
                        "file test/data/01_file.txt seen before: "
                        "('#', 'test/data/**/0?_*.txt')",
                        "file test/data/02_file.txt seen before: "
                        "('#', 'test/data/**/0?_*.txt')"
                    ]
                    }
                ]
            },
        )
        )

    def testCheckOk(self):
        self.maxDiff = 1_000_000_000
        expected = chain(
            _TEST_DATA_DIR / "02_config.yaml",
            read_config,
            scan_globs)
        actual = check_files(expected)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
