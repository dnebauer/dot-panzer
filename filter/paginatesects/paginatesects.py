#!/usr/bin/env python3
"""
Add page break at the start of each H1 section

    --- page break ---

    # Section

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
# pylint: disable=wrong-import-position,import-error, unused-import
import panzertools  # NOQA
from pandocfilters import RawInline, Para, Header, toJSONFilter  # NOQA


# method signature for rehead determined by pandocfilters
# - format is redefined, meta is unused
# pylint: disable=redefined-builtin,unused-argument
def rehead(key, value, format, meta):
    """ Insert newpage before each Header 1
    """
    if key == 'Header' and value[0] == 1:
        if format == 'latex':
            text = '\\newpage\n\\thispagestyle{empty}\n\\setcounter{page}{1}'
            return [Para([RawInline('latex', text)]),
                    Header(value[0], value[1], value[2])]
        elif format in ['html', 'html5']:
            text = '<hr>'
            return [Para([RawInline('html', text)]),
                    Header(value[0], value[1], value[2])]


if __name__ == "__main__":
    panzertools.log('INFO', 'adding page break before each H1 section')
    toJSONFilter(rehead)
