#!/usr/bin/env python3
"""
Include the contents of other markdown files.

This filter looks for file-include directives and processes them.

Each directive is a standalone paragraph consisting of a directive
keyword and value, which can be separated by whitespace, colon
and/or equals sign, e.g.:

    KEYWORD value
    KEYWORD:value
    KEYWORD: value
    KEYWORD : value
    KEYWORD=value
    KEYWORD= value
    KEYWORD = value

Note that, as each directive is its own paragraph, it must be
preceded and followed by at least one blank line.

Directive keywords are all uppercase.

The directives are:

INCLUDEPREFIX path

The provided path will be prepended to any include file's file
path.

If no path is provided the existing prefix path is unset. If
no prefix path is currently set, this directive has no effect.

If an invalid path is provided this directive has no effect,
and an error message is generated.

The prefix path can be relative or absolute.

If this directive is successfully processed it is removed from
any generated output; if not, it is left in the generated output.

INCLUDEFILE filepath

The provided filepath is that of a markdown file whose content
replaces the directive paragraph.

If a prefix path has been set before this directive is
encountered, it is prepended to the include file's filepath.

Error messages are generated if the directive has no filepath
value, or the provided filepath (plus prepended prefix if set)
is invalid.

The include file's filepath can be absolute or relative. If a
prefix path has been set, only relative include file filepaths
can be used.

If this directive is successfully processed it is replaced with
the contents of the specified include file; if not, it is left
in the generated output.
"""

from __future__ import print_function
import sys
import os
if 'PANZER_SHARED' not in os.environ:  # exit with error message
    print('ERROR: Requires PANZER_SHARED environmental variable',
          file=sys.stderr)
    print('WARNING: This filter is designed to be run by panzer',
          file=sys.stderr)
    quit(1)
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
# pylint: disable=wrong-import-position,import-error,unused-import
from pandocfilters import toJSONFilter, stringify  # NOQA
import panzertools  # NOQA
import panzerutils  # NOQA


def include_file_content(value):
    """ Extract content of include file in json format

    Relies on panzerutils function 'mdfile_to_json' to extract
    content of include file.

    Params:
    - value: original object value supplied by toJSONfilter()

    Returns:
    * Return values are ultimately for toJSONfilter, so its behaviour
      determines the choice of return values
    - Success: json-formatted content of include file
    - Failure: None (which means original value remains unchanged)
    """
    filepath = extract_path('INCLUDEFILE', value)
    if not filepath:  # deal with empty filepath
        panzertools.log('ERROR', 'no file path in directive: "' +
                        stringify(value) + '"')
        return None  # keep original object value from toJSONfilter()
    fullpath = filepath
    if include_directives.prefix:  # add prefix if set
        fullpath = os.path.join(include_directives.prefix, filepath)
    if not os.path.lexists(fullpath):  # check validity of path
        panzertools.log('ERROR', 'invalid include file path: ' + fullpath)
        return None  # keep original object value from toJSONfilter()
    # valid path, so return file content in json format
    panzertools.log('INFO', 'including file: ' + fullpath)
    return panzerutils.mdfile_to_json(fullpath)  # json content


def include_prefix(value):
    """ Set or unset include prefix path

    This path is prefixed to all subsequent include file paths.

    If a valid path is specified it is set.
    If an invalid path is specified the prefix is left unchanged.
    If no path is provided the prefix is unset.

    Params:
    - value: original object value supplied by toJSONfilter()

    Returns:
    * Return values are ultimately for toJSONfilter, so its behaviour
      determines the choice of return values
    - Success: [] (which means original value is deleted)
    - Failure: None (which means original value remains unchanged)
    """
    path = extract_path('INCLUDEPREFIX', value)
    if not path:  # no path provided so unset prefix if set
        if include_directives.prefix:
            include_directives.prefix = str()
            panzertools.log('INFO', 'prefix unset')
        return []  # delete original value
    if not os.path.lexists(path):  # invalid path
        panzertools.log('ERROR', 'prefix path is invalid: ' + path)
        return None  # keep original object value from toJSONfilter()
    # valid path so set prefix
    include_directives.prefix = path
    panzertools.log('INFO', 'prefix set to:')
    panzertools.log('INFO', '- "' + path + '"')
    return []  # delete original value


def extract_path(keyword, value):
    """ Extracts path from supplied ast object value

    Must cope with following cases:
    'KEYWORD path'
    'KEYWORD: path'
    'KEYWORD : path'
    'KEYWORD=path'
    'KEYWORD = path'

    All spaces may be multiple and consist of any whitespace characters.
    The path itself may contain spaces which are preserved.

    Params:
    - keyword: keyword at head of stringified value
    - value: original value supplied by toJSONfilter()

    Returns:
    - Valid path extracted: path as string
    - Invalid path extracted: False
    - No path extracted: None
    """
    # extract path from stringified value
    begin = len(keyword)
    string = stringify(value)
    raw_path = string[begin:]
    path = raw_path.strip(' :=\t\n\r')
    return path


# method signature is determined by pandocfilters, so can't
# help that 'format' and 'meta' are unused
# pylint: disable=redefined-builtin,unused-argument
# each return statement does, in fact, return an expression
# pylint: disable=inconsistent-return-statements
def include_directives(key, value, format, meta):
    """ Looks for include directives and processes them

    Include directives are INCLUDEFILE and INCLUDEPREFIX:
    - INCLUDEFILE specifies file whose content is to be inserted
    - INCLUDEPREFIX specifies path to be prefixed to include file paths

    Params:
    - as specified by toJSONfilter()

    Returns:
    * Return values are ultimately for toJSONfilter, so its behaviour
      determines the choice of return values
    - If include file:
      . Success: json-formatted content of include file
      . Failure: None (which means original value remains unchanged)
    - If include prefix:
      . Success: [] (which means original value is deleted)
      . Failure: None (which means original value remains unchanged)
    """
    if (key == 'Para' and value[0]['t'] == 'Str'):
        first_string = value[0]['c']
        if first_string.startswith('INCLUDEFILE'):
            return include_file_content(value)
        if first_string.startswith('INCLUDEPREFIX'):
            return include_prefix(value)


include_directives.prefix = str()


if __name__ == "__main__":
    toJSONFilter(include_directives)
