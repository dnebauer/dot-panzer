#!/usr/bin/env python3
"""
open pdf file produced by latexmk
"""

import os
import subprocess
import sys
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools


def open_pdf(filepath):
    """Use xdg-open to open pdf file"""
    fullpath = os.path.abspath(filepath)
    subprocess.check_output(["xdg-open", fullpath],
                            stderr=subprocess.STDOUT)


def main():
    """docstring for main"""
    options = panzertools.read_options()
    filepath = options['pandoc']['output']
    if filepath == '-':
        panzertools.log('INFO', 'not run')
        return
    target = panzertools.FileInfo(filepath)
    target.set_extension('.pdf')
    pdfpath = target.fullpath()
    if os.path.exists(pdfpath):
        open_pdf(pdfpath)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
