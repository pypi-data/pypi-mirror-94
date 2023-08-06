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
import unittest

from setup_headers.main import main
from setup_headers.process import FileNotInPrefixes


class Test(unittest.TestCase):

    def testRunDry(self):
        main("--dry-run".split())

    def testRunDryFiles(self):
        main("--dry-run test/data/01_file.txt "
             "test/data/02_file.txt".split())

    def testInvalidConfig(self):
        with self.assertRaises(SystemExit) as e:
            main('--config ZZZZZZ'.split())
        self.assertEqual(e.exception.args, (2,))

    def testPrefixMandatory(self):
        with self.assertRaises(FileNotInPrefixes) as e:
            main('--prefix-mandatory requirements-dev.txt'.split())
        self.assertEqual(e.exception.args, (['requirements-dev.txt'],))

    def testNoPrefixMandatory(self):
        main('requirements-dev.txt'.split())
        main('--dry-run requirements-dev.txt'.split())
