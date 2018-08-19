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

The value in each case is a directory or file path. These paths can be
formatted as links:

    KEYWORD: [value]()

For reasons not currently understood, these directives can cause syntax
highlighting to fail. In many cases, though not all, formatting paths as links
preserves syntax highlighting. Since formatting as links results in them being
colored as a result of syntax highlighting, this may improve the appearance and
readability of the document.

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


def include_file_content(path):
    """ Extract content of include file in json format

    Relies on panzerutils function 'mdfile_to_json' to extract
    content of include file.

    Params:
    - path: path to include file

    Returns:
    * Return values are ultimately for toJSONfilter, so its behaviour
      determines the choice of return values
    - Success: json-formatted content of include file
    - Failure: None (which means original value remains unchanged)
    """
    if path is None:  # deal with empty filepath
        panzertools.log('ERROR', 'no file path in INCLUDEFILE directive')
        return None  # keep original object value from toJSONfilter()
    if include_directives.prefix:  # add prefix if set
        path = os.path.join(include_directives.prefix, path)
    if os.path.lexists(path):  # return file content in json format
        panzertools.log('INFO', 'including file: ' + path)
        return panzerutils.mdfile_to_json(path)
    # if here then invalid path
    panzertools.log('ERROR', 'invalid include file path: ' + path)
    return None  # keep original object value from toJSONfilter()


def include_prefix(path):
    """ Set or unset include prefix path

    This path is prefixed to all subsequent include file paths.

    If a valid path is specified it is set.
    If an invalid path is specified the prefix is left unchanged.
    If no path is provided the prefix is unset.

    Params:
    - path: include file prefix

    Returns:
    * Return values are ultimately for toJSONfilter, so its behaviour
      determines the choice of return values
    - Success: [] (which means original value is deleted)
    - Failure: None (which means original value remains unchanged)
    """
    if path is None:  # no path provided so unset prefix if set
        if include_directives.prefix:
            include_directives.prefix = str()
            panzertools.log('INFO', 'prefix unset')
        return []  # delete original value
    if os.path.lexists(path):  # valid path so set prefix
        include_directives.prefix = path
        panzertools.log('INFO', 'prefix set to: ' + path)
        return []  # delete original value
    # if here then invalid path
    panzertools.log('ERROR', 'prefix path is invalid: ' + path)
    return None  # keep original object value from toJSONfilter()


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
        string = stringify(value)
        if string.startswith(('INCLUDEFILE', 'INCLUDEPREFIX')):
            directive, val = panzerutils.key_value_pair(string)
            if directive == 'INCLUDEFILE':
                return include_file_content(val)
            elif directive == 'INCLUDEPREFIX':
                return include_prefix(val)
            return None  # not a directive; keep toJSONfilter() object value


include_directives.prefix = str()


if __name__ == "__main__":
    toJSONFilter(include_directives)
