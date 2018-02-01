#!/usr/bin/env python3

"""
Panzer postflight script: create mobi file from epub
    Uses 'calibre' cli utility 'ebook-convert'.

    There appears to be a problem with how calibre handles (at least some)
    pandoc-created epub when converting it to mobi -- it strips out the
    cover image. (Turn on conversion feedback and see error message on
    screen and in the panzer log.)

    As a workaround, use same algorithm as the inject_epub_cover filter
    to look for cover image file in current directory -- is named
    '<epub_basename>.{png,gif,jpg}'. If present, assume there is a cover
    image in the epub output, so have calibre strip out first image
    (presumed to be the cover image) and insert the detected cover image
    file.
"""

from __future__ import print_function
import os
import subprocess
import sys
if 'PANZER_SHARED' not in os.environ:  # exit with error message
    print('ERROR: Requires PANZER_SHARED environmental variable',
          file=sys.stderr)
    print('WARNING: This script is designed to be run by panzer',
          file=sys.stderr)
    quit(1)
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
# pylint: disable=wrong-import-position,import-error, unused-import
import panzertools  # NOQA
import panzerutils  # NOQA


def main():
    """ Main script logic
    """
    # need calibre
    ebook_convert = calibre_cli_executable()
    if not ebook_convert:
        log('INFO', 'calibre not available')
        return
    # need epub file to convert
    options = panzertools.read_options()
    output_dir, epub = os.path.split(options['pandoc']['output'])
    output_basename = os.path.splitext(epub)[0]
    if not os.path.exists(epub):
        log('INFO', epub + ' not available to convert')
        return
    log('DEBUG', 'epub file: ' + epub)
    # get target mobi file name
    mobi = output_basename + '.mobi'
    log('DEBUG', 'mobi file: ' + mobi)
    # check for cover image (see module docstring)
    cover_image = panzerutils.image_file(output_dir, output_basename)
    # create mobi output file
    create_mobi_output(ebook_convert, output_basename, cover_image)


def calibre_cli_executable():
    """ Get name of calibre command-line executable
    """
    # get name of calibre executable for os/platform
    # - for now assume is same on all systems
    calibre_cli = 'ebook-convert'
    # check if calibre executable is available on system
    exe = panzerutils.which(calibre_cli)
    if not exe:
        log('DEBUG', 'calibre executable ' + str(exe) + ' not available')
        return
    return exe


def create_mobi_output(ebook_convert, basename, cover_image):
    """ Create mobi output file
        See module docstring for explanation of arguments used to
        add a cover image to the output file.
    """
    epub = basename + '.epub'
    mobi = basename + '.mobi'
    command = [ebook_convert, epub, mobi]
    if cover_image:
        command.extend(['--remove-first-image', '--cover', cover_image])
    try:  # to generate output
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout_bytes, stderr_bytes = proc.communicate()
        encoding = panzertools.ENCODING
        if stdout_bytes:
            stdout = stdout_bytes.decode(encoding, errors='ignore')
            for line in stdout.splitlines():
                log('DEBUG', line)
        if stderr_bytes:
            stderr = stderr_bytes.decode(encoding, errors='ignore')
            for line in stderr.splitlines():
                log('DEBUG', line)
    except OSError as error:
        log('ERROR', error)


def log(level, msg):
    """ Print log message to panzer log
    """
    panzertools.log(level, msg)


if __name__ == '__main__':
    main()
# vim:fdm=indent:
