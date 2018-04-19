#!/usr/bin/env python3
"""
Panzer filter: add metadata files from styles
    Add metadata files specified by 'metadata-file' field in metadata.
    Metadata files are markdown files containing a yaml metadata block.

    The 'metadata-file' field can be a single inline value or a list
    of multiple values:

        metadata-file: my-file.md

        OR

        metadata-file:
          - my-file-1.md
          - my-file-2.md

    In any given metadata block only the last 'metadata-file' field has
    any effect, so to specify multiple files use the list format.

    Metadata files can be specified in the source input file or the
    panzer style file (default path: $HOME/.panzer/styles/styles.yaml).
    In the style file metadata files can be specfied in the metadata
    blocks for style output formats.

    'metadata-file' fields from different metadata blocks are additive.
    The way in which these files are processed ensure that if the same
    setting is specified in multiple metadata files, the last one
    processed will 'win'. The exception is 'header-includes' fields
    which are cumulative.
    
    Metadata from files specified in the source (markdown) file is
    processed after that from files specified in the style file, so in
    case of conflict the source file 'beats' the style file. Note that
    if the source (markdown) file has a 'header-includes' field it will
    *not* be cumulative with the 'header-includes' values from the
    previously read metadata files -- it will completely replace them.

    A metadata file can be specified by a full path, either full or
    relative to the current working directory. If the file is not a
    valid path, the filter looks for the file in the current
    directory, then in directory '$HOME/.config/panzer/custom' (this
    is a non-standard location for the entire panzer tree which is
    usually in '$HOME/.panzer' and has the non-standard subdirectory
    'custom'), and finally in directory '$HOME/.panzer/custom' (where
    the panzer tree is in the default location but with the
    non-standard subdirectory 'custom'). The first matching file
    found is used, i.e., the first match wins.

    *WARNING*: If other filters to be called rely on metadata
               obtained via this filter, ensure this filter is
               called before them. It is strongly recommended this
               filter is the first one specified.

    The main work of this filter is done by the PandocAST class
    found in '$HOME/.panzer/shared/python/panzerutils.py'.
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
# pylint: disable=wrong-import-position,import-error
import panzerutils  # NOQA


def main():
    """ panzerutils: $HOME/.panzer/shared/python/panzerutils.py
    """
    ast = panzerutils.PandocAST()
    ast.load_extra_metadata()
    ast.write()


if __name__ == '__main__':
    main()
# vim:fdm=indent:
