#!/usr/bin/env python3
"""
Looks for file include statements and replaces them with the
contents of the include file.

The include file statement has the format:

    INCLUDEFILE filepath

where 'INCLUDEFILE' starts a paragraph and the remainder of the
paragraph is the filepath. The space immediately following the
'INCLUDEFILE' keyword is ignored, but all other spaces on the line
are assumed to be part of the filepath and are preserved.

If a filepath is provided and is valid, the paragraph is replaced
by the content of the include file. This must be a markdown file.

If no valid filepath is provided, the include file statement is
left in the output 'as is' and an error message generated.
Depending on the settings used this may halt processing.
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
from pandocfilters import toJSONFilter  # NOQA
import panzertools  # NOQA
import panzerutils  # NOQA


# method signature is determined by pandocfilters, so can't
# help that 'format' and 'meta' are unused
# pylint: disable=redefined-builtin,unused-argument
# each return statement does, in fact, return an expression
# pylint: disable=inconsistent-return-statements
def includefiles(key, value, format, meta):
    """ Looks for include file statements and inserts file content

    Looks for a line 'INCLUDEFILE filepath'.
    Relies on panzerutils function 'mdfile_to_json' to extract
    content of include file.
    """
    if (key == 'Para' and value[0]['t'] == 'Str' and
            value[0]['c'] == 'INCLUDEFILE'):
        # assume followed by space element and at least one string element
        if len(value) > 2 and value[1]['t'] != 'Space':
            panzertools.log('ERROR', 'Invalid value: ' + value)
            return value
        # extract filepath
        filepath = str()
        # - not interested in INCLUDEFILE ([0]) or following space ([1])
        # - capture spaces that are presumed to be part of filepath
        for element in value[2:]:
            if element['t'] == 'Str':
                filepath += element['c']
            elif element['t'] == 'Space':
                filepath += ' '
        # check that file is valid
        if not os.path.lexists(filepath):
            panzertools.log('ERROR', 'Invalid filepath: ' + filepath)
            return value
        panzertools.log('INFO', 'Include file: ' + filepath)
        # return file content in json format
        content = panzerutils.mdfile_to_json(filepath)
        return content


if __name__ == "__main__":
    toJSONFilter(includefiles)
