#!/usr/bin/env python3

"""
Reset the header level for the document

- new base level is value passed in argv[2]
- base level values may be from 1 to 5

if 2 is passed then:

    # Section

is transformed to -->

    ## Section

"""

import sys
import os
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools
from pandocfilters import toJSONFilter, Header

NEW_LEVEL = 1


def rehead(key, value, format, meta):
    """docstring for rehead"""
    if key == 'Header':
        return Header(NEW_LEVEL + (value[0] - 1), value[1], value[2])


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        NEW_LEVEL = max(min(5, int(sys.argv[2])), 1)
    panzertools.log('INFO', 'base header level set to %d' % NEW_LEVEL)
    toJSONFilter(rehead)
