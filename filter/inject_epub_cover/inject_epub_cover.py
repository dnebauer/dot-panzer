#!/usr/bin/env python3
"""
Panzer filter: add cover image to epub output
    If epub cover image is present in directory,
    add appropriate command to metadata.

    Cover image file has same base name as markdown file with extension
    being either png, gif or jpg. If multiple cover image files are
    available, preference is png > gif > jpg.

    Example:

    ---
    title: "My first book"
    author: John Citizen
    ---

    to

    ---
    title: "My first book"
    author: John Citizen
    cover-image: my-book.png
    ---
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
import panzertools  # NOQA
import panzerutils  # NOQA

ENCODING = 'utf-8'


def main():
    """ panzerutils: $HOME/.panzer/shared/python/panzerutils.py
    """
    ast = panzerutils.PandocAST()
    # check whether cover image set on command line or in metadata
    epub_cover_set = ast.epub_cover_set()
    if epub_cover_set:
        log('INFO', 'cover image set ' + epub_cover_set)
        ast.write()
        return
    log('DEBUG', 'cover image not set in metadata or command line')
    # set local cover image if available
    epub_cover = ast.epub_cover_local()
    if epub_cover:
        log('INFO', 'cover image: ' + epub_cover)
        ast.epub_cover_add()
    else:
        log('INFO', 'no cover image located')
    ast.write()


def log(level, msg):
    """ Print log message to panzer log
    """
    panzertools.log(level, msg)


if __name__ == '__main__':
    main()
# vim:fdm=indent:
