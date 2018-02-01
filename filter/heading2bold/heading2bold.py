#!/usr/bin/env python3

"""
Change the H1, H2 heading to bold and italics respectively

    # Section 1

    ## Section 2

is transformed to -->

    **Section 1**

    *Section 2*

"""

from pandocfilters import RawInline, Strong, Para, Emph, toJSONFilter


def latex(content):
    """docstring for latex"""
    return RawInline('latex', content)


def rehead(key, value, format, meta):
    """docstring for rehead"""
    if key == 'Header' and value[0] == 1:
        return Para([latex('\\vspace{1em}')] + [Strong(value[2])])
    if key == 'Header' and value[0] == 2:
        return Para([Emph(value[2])])


if __name__ == "__main__":
    toJSONFilter(rehead)
