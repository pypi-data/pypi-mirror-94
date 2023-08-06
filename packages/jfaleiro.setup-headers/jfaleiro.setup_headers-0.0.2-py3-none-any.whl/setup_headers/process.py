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

import functools
import itertools
import os
import pathlib
import re

import glom
import yaml
from cerberus import Validator

DEFAULT_CONFIG_FILE = 'headers.yaml'
DEFAULT_HEADER = 'HEADER'


def chain(arg, *f):
    return functools.reduce(lambda x, f: f(x), f, arg)


def readlines(file_name):
    if not os.path.isfile(file_name):
        raise FileNotFoundError(file_name)
    with open(file_name) as f:
        return [line.strip('\n') for line in f.readlines()]


def process_lines(header_lines, lines, comment_prefix):
    result = []
    phases = ('adding_hashbangs',
              'removing_previous_comments',
              'adding_header',
              'adding_source')
    phase = phases[0]
    for line in lines:
        assert phase in phases, '%s not in %s' % (phase, phases)
        if phase == phases[0]:
            if line.startswith('#!'):
                result.append(line)
            else:
                phase = phases[1]
        if phase == phases[1]:
            if line.startswith(comment_prefix[0]):
                pass
            else:
                phase = phases[2]
        if phase == phases[2]:
            result.extend([comment_prefix + line for line in header_lines])
            phase = phases[3]
        if phase == phases[3]:
            result.append(line)
    return result


class AbsolutePathError(Exception):
    pass


def files_for_pattern(pattern) -> set:
    if os.path.isabs(pattern):
        raise AbsolutePathError(pattern)
    return [str(f)
            for f in pathlib.Path('.').glob(pattern)]


def modify_file(dry_run, header_lines, prefix, filename):
    assert isinstance(filename, str)
    assert isinstance(header_lines, list)

    lines = readlines(filename)
    output = process_lines(header_lines, lines, prefix)
    if lines != output:
        print(f'adjusting {filename}, prefix={prefix}, '
              f'{len(lines)}/{len(output)} lines before/after')
        if not dry_run:
            with open(filename, 'w') as file:
                for line in output:
                    file.write(line + '\n')
        return True
    return False


class InvalidPatternInPrefixes(Exception):
    pass


class PrefixDefinedMoreThanOnce(Exception):
    pass


class NoFilesForExpression(Exception):
    pass


class NoFilesForExpressionAfterExclude(Exception):
    pass


class FilesAssociatedToPrefixBefore(Exception):
    pass


class ConfigurationValidationError(Exception):
    pass


class FileParsingValidationError(Exception):
    pass


def duplicates(items: list) -> set:
    return set([x for x in items
                if items.count(x) > 1])


def read_config(file):
    class CustomValidator(Validator):
        def _check_with_header_exists(self, field, value):
            if not os.path.isfile(self.document['header']):
                self._error(field,
                            f'header file "{self.document["header"]}" '
                            'is not a file or does not exist')

        def _check_with_glob_unique(self, field, value):
            globs = [g for g in [x['globs']
                                 for x in self.document['prefixes']]]
            d = duplicates(list(itertools.chain(*globs)))
            if len(d) > 0:
                self._error(field, f'glob {d} defined more than once')

        def _check_with_prefix_unique(self, field, value):
            prefixes = [x['prefix'] for x in self.document['prefixes']]
            d = duplicates(prefixes)
            if len(d) > 0:
                self._error(field, f'prefix {d} defined more than once')

    with open(file, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    validator = CustomValidator(
        dict(
            header=dict(
                type='string',
                default=DEFAULT_HEADER,
                check_with="header_exists"
            ),
            excludes=dict(
                type='list',
                default=list(),
            ),
            prefixes=dict(
                type='list',
                default=list(),
                check_with=('prefix_unique', 'glob_unique'),
                schema=dict(
                    required=True,
                    type='dict',
                    schema=dict(
                        prefix=dict(
                            type='string',
                            required=True,
                        ),
                        globs=dict(
                            type='list',
                            required=True,
                            schema=dict(
                                type='string',
                                required=True
                            )
                        )
                    )
                )
            )
        )
    )
    normalized = validator.normalized(config)
    if not validator.validate(normalized):
        raise ConfigurationValidationError(validator.errors)
    return normalized


def scan_globs(
        config,
        readlines_function=readlines,
        glob_function=files_for_pattern):

    def globs(globs, regex_excludes):
        regexes = [re.compile(regex) for regex in regex_excludes]

        def values(glob):
            files = sorted(glob_function(glob))
            return dict(
                files_before_excludes=files,
                files=sorted([
                    file for file in files if all(
                        [not regex.match(file) for regex in regexes]
                    )])
            )
        return {glob: values(glob) for glob in globs}

    return glom.glom(
        config,
        dict(
            header=dict(
                name='header',
                content=('header', readlines_function),
                excludes='excludes',
                prefixes=(
                    'prefixes',
                    [
                        dict(
                            prefix='prefix',
                            globs=(
                                'globs',
                                lambda g: globs(
                                    g,
                                    glom.glom(
                                        config, 'excludes'
                                    )
                                )
                            )
                        )
                    ]
                )
            )
        )
    )


def check_files(config):
    class CustomValidator(Validator):
        def _check_with_files_not_associated_with_prefix_before(self, field,
                                                                value):
            file_prefix = dict()
            for prefix_globs in value:
                prefix, globs = prefix_globs['prefix'], prefix_globs['globs']
                for glob, matches in globs.items():
                    files, before_exclusion = (
                        matches['files'],
                        matches['files_before_excludes']
                    )
                    if len(before_exclusion) == 0:
                        self._error(field, f'no files for glob {glob}')
                    elif len(files) == 0:
                        self._error(field,
                                    f'no files for glob {glob} '
                                    f'after excludes')
                    else:
                        for file in before_exclusion:
                            if file in file_prefix:
                                self._error(
                                    field,
                                    f'file {file} seen before: '
                                    f'{file_prefix[file]}'
                                )
                            file_prefix[file] = (prefix, glob)

    validator = CustomValidator(
        dict(
            header=dict(
                type='dict',
                schema=dict(
                    name=dict(
                        type="string",
                        empty=False
                    ),
                    content=dict(
                        type="list",
                        empty=False
                    ),
                    excludes=dict(
                        type="list",
                    ),
                    prefixes=dict(
                        type="list",
                        empty=False,
                        check_with='files_not_associated_with_prefix_before',
                        schema=dict(
                            type='dict',
                            schema=dict(
                                prefix=dict(
                                    type='string',
                                    empty=False
                                ),
                                globs=dict(
                                    type='dict',
                                    empty=False,
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    if not validator.validate(config):
        raise FileParsingValidationError(validator.errors)

    return config


def _apply_prefixes(prefixes, callback):
    for prefix_globs in prefixes:
        prefix, globs = prefix_globs['prefix'], prefix_globs['globs']
        for glob, matches in globs.items():
            for file in matches['files']:
                callback(
                    prefix=prefix,
                    file=file
                )


def update_files(config, dry_run, modify_function=modify_file):
    content = glom.glom(config, 'header.content')

    if dry_run:
        print('dry run, no changes to be applied')

    def callback(prefix, file):
        modified = modify_function(dry_run=dry_run,
                                   header_lines=content,
                                   prefix=prefix,
                                   filename=file)
        if modified:
            callback.modifications += 1
    callback.modifications = 0
    _apply_prefixes(
        prefixes=glom.glom(config, 'header.prefixes'),
        callback=callback
    )
    return callback.modifications


class FileNotInPrefixes(Exception):
    pass


def update_file(config, dry_run, files, prefix_mandatory,
                modify_function=modify_file):
    content = glom.glom(config, 'header.content')

    def callback(prefix, file):
        if file in files:
            modify_function(dry_run=dry_run,
                            header_lines=content,
                            prefix=prefix,
                            filename=file)
            callback.updates.add(file)
    callback.updates = set()
    _apply_prefixes(
        prefixes=glom.glom(config, 'header.prefixes'),
        callback=callback
    )
    difference = files - callback.updates
    if len(difference) != 0:
        if prefix_mandatory:
            raise FileNotInPrefixes(list(difference))

    return len(callback.updates)


def process_all(args) -> None:
    chain(
        args.config,
        read_config,
        scan_globs,
        check_files,
        lambda config: update_files(config=config,
                                    dry_run=args.dry_run)
    )


def process_file(args) -> None:
    chain(
        args.config,
        read_config,
        scan_globs,
        check_files,
        lambda config: update_file(
            config=config,
            dry_run=args.dry_run,
            prefix_mandatory=args.prefix_mandatory,
            files=args.files
        )
    )
