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
from pathlib import Path

from setup_headers.process import (chain, read_config, readlines, scan_globs,
                                   update_file)

_TEST_DATA_DIR = Path('test')/'data'/'config'


class Test(unittest.TestCase):

    def testDryRun(self):
        expected_modifications = 1
        config = _TEST_DATA_DIR / '02_config.yaml'
        self.assertEqual(chain(
            config,
            read_config,
            scan_globs,
            lambda config: update_file(config=config,
                                       dry_run=True,
                                       prefix_mandatory=True,
                                       files=set(['test/data/01_file.txt'])
                                       )
        ), expected_modifications)

        # dry runs should yield the same number of modifications
        self.assertEqual(chain(
            config,
            read_config,
            scan_globs,
            lambda config: update_file(config=config,
                                       dry_run=True,
                                       prefix_mandatory=True,
                                       files=set(['test/data/01_file.txt'])
                                       )
        ), expected_modifications)

    def testRun(self):
        with tempfile.TemporaryDirectory(dir='build') as temp_dir:
            config = dict(
                header="test/data/02_header.txt",
                excludes=[],
                prefixes=[
                    dict(prefix="#",
                         globs=[
                             os.path.join(temp_dir,
                                          "01_*.txt")
                         ])
                ])
            shutil.copy("test/data/01_file.txt", temp_dir)
            count = chain(
                config,
                scan_globs,
                lambda config: update_file(config=config,
                                           dry_run=False,
                                           prefix_mandatory=True,
                                           files=set([os.path.join(
                                               temp_dir,
                                               "01_file.txt")])
                                           )
            )
            self.assertEqual(count, 1)
            self.assertEqual(readlines(os.path.join(temp_dir,
                                                    "01_file.txt")),
                             readlines("test/data/02_expected.txt"))


if __name__ == "__main__":
    unittest.main()
