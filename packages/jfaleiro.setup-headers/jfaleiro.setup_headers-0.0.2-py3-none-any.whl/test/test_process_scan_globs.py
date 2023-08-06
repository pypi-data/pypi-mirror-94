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
from pathlib import Path

from glom import glom
from setup_headers.process import AbsolutePathError, scan_globs

_TEST_DATA_DIR = Path('test')/'data'/'config'


class Test(unittest.TestCase):

    def testGlom(self):
        target = {'header': 'HEADER',
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
                       'prefix': '//'}]}

        expected = dict(
            header=dict(
                name='HEADER',
                content='<...content...>',
                prefixes=dict(
                    prefix='#',
                    globs=dict(glob='**',
                               files=['file1', 'file2'])
                )
            )
        )

        def readlines(file):
            return '<...content...>'

        def build_prefixes(node):
            return dict(
                prefix=node[0]['prefix'],
                globs=dict(
                    glob='**',
                    files=['file1', 'file2']))

        spec = dict(
            header=dict(
                name='header',
                content=('header', readlines),
                prefixes=('prefixes', build_prefixes)
            )
        )
        self.assertEqual(glom(target, spec),
                         expected)

    def testExpandPrefixes(self):
        actual = scan_globs(
            {
                'header': 'test/data/02_header.txt',
                'excludes': [],
                'prefixes': [
                    {
                        'prefix': '#',
                        'globs': [
                            'test/data/**/02_e*.txt'
                        ]
                    },
                    {
                        'prefix': '##',
                        'globs': [
                            'test/data/**/02_f*.txt',
                            'test/data/**/01_f*.txt'
                        ]
                    }
                ]
            }
        )
        expected = {
            'header': {
                'name': 'test/data/02_header.txt',
                'content': [' header 1', ' header 2  '],
                'excludes': [],
                'prefixes': [
                    {'prefix': '#',
                     'globs': {
                         'test/data/**/02_e*.txt': {
                             'files_before_excludes': [
                                 'test/data/02_expected.txt'
                             ],
                             'files': [
                                 'test/data/02_expected.txt'
                             ]
                         }
                     }
                     }, {
                         'prefix': '##',
                         'globs': {
                             'test/data/**/02_f*.txt': {
                                 'files_before_excludes': [
                                     'test/data/02_file.txt'
                                 ],
                                 'files': [
                                     'test/data/02_file.txt'
                                 ]
                             },

                             'test/data/**/01_f*.txt': {
                                 'files_before_excludes': [
                                     'test/data/01_file.txt'
                                 ],
                                 'files': [
                                     'test/data/01_file.txt'
                                 ]
                             }
                         }
                    }
                ]
            }
        }
        self.assertEqual(actual, expected)

    def testExcludes(self):
        self.maxDiff = None
        actual = scan_globs(
            {
                'header': 'test/data/02_header.txt',
                'excludes': [
                    '^.*02_expected',
                    '^.*file'
                ],
                'prefixes': [
                    {
                        'prefix': '#',
                        'globs': [
                            'test/data/**/02_*.txt'
                        ]
                    },
                ]
            }
        )
        expected = {
            'header': {
                'name': 'test/data/02_header.txt',
                'content': [' header 1', ' header 2  '],
                'excludes': [
                    '^.*02_expected',
                    '^.*file'
                ],
                'prefixes': [
                    {
                        'prefix': '#',
                        'globs': {
                            'test/data/**/02_*.txt': {
                                'files_before_excludes': [
                                    'test/data/02_expected.txt',
                                    'test/data/02_file.txt',
                                    'test/data/02_header.txt'
                                ],
                                'files': [
                                    'test/data/02_header.txt'
                                ]
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(actual, expected)

    def testAbsolutePathsInPrefixes(self):
        config = dict(header='test/data/02_header.txt',
                      excludes=[],
                      prefixes=[
                          dict(prefix='#',
                               globs=["/tmp/*.txt"])
                      ])
        with self.assertRaises(AbsolutePathError) as e:
            scan_globs(config)
        self.assertEqual(e.exception.args, ("/tmp/*.txt",))

    def testHeaderNotAFile(self):
        with self.assertRaises(FileNotFoundError) as e:
            scan_globs(config=dict(header='test'))
        self.assertEqual(e.exception.args, ("test", ))

    def testHeaderDoesNotExist(self):
        with self.assertRaises(FileNotFoundError) as e:
            scan_globs(config=dict(header='does_not_exist.yaml'))
        self.assertEqual(e.exception.args, ("does_not_exist.yaml", ))


if __name__ == "__main__":
    unittest.main()
