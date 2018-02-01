#!/usr/bin/env python3
"""
Makes ordered lists between open and close div tags one big list.
Picks the first ordered list type it hits after opening tag as the list to
match on.

Example:

    <div class="singlelist">
    1. hello
    2. there

    more text

    1. hello again
    2. there again
    </div>

-- filter transforms to ->>>:
    1. hello
    2. there

    more text

    3. hello again
    4. there again
"""

from pandocfilters import toJSONFilter


def transform_div(key, value, format, meta):
    """docstring stub"""
    if key == 'Div' and "singlelist" in value[0][1]:
        return make_singlelist(value[1], None)


def make_singlelist(lst, pat):
    """docstring stub"""
    if lst == []:
        return []
    head = lst[0]    # head
    tail = lst[1:]  # tail
    if isinstance(head, dict) and 't' in head and head['t'] == 'OrderedList':
        spec = list(head['c'][0])
        items = list(head['c'][1])
        if pat is None:
            # if first list hit, use as the pattern to match on
            pat = spec
            offset = len(items)
            pat[0] += offset
        elif spec[1] == pat[1] and spec[2] == pat[2]:
            # if spec matches current pattern, then increment start number
            head['c'][0][0] = pat[0]
            offset = len(items)
            pat[0] += offset
    return [head] + make_singlelist(tail, pat)


if __name__ == "__main__":
    toJSONFilter(transform_div)
