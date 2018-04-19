# this should be run with Python 3

""" Utilities for custom panzer setup """

import sys
import os
import json
import subprocess
import pprint
import yaml

ENCODING = 'utf8'


class PandocAST(object):
    """ Read, manipulate and write pandoc ast
    """

    def __init__(self, data=None):
        """ Read ast and extract key values
            Sets these internal variables:
            - self.__ast = entire ast
            - self.__meta = ast's 'meta' key value
            - self.__json_msg = embedded panzer json_msg
            --> self.__ast contains self.__meta,
                which itself contains self.__json_msg
            - self.__metadata_files = metadata filepaths
            - self.__metadata_new = newly generated metadata
            - self.__epub_cover_image
        """
        # self.__ast :: read in ast
        self.__ast = str()
        if data:
            self.__ast = data
        else:
            self.__ast = json.load(sys.stdin)
            log('DEBUG', 'reading ast')

        # self.__meta :: extract meta content
        # - must exist and have content (contains panzer_reserved)
        try:
            self.__meta = self.__ast['meta']
        except KeyError:
            log('DEBUG', 'ast has no meta key')
            raise
        if not self.__meta:
            log('DEBUG', 'no meta content in ast')
            raise ValueError('ast meta key has no content')

        # self.__json_msg :: panzer's JSON_MESSAGE
        self.__json_msg = json.loads(self.__meta['panzer_reserved']['c']
                                     ['json_message']['c'][0]['c'][1])[0]

        # self.__metadata_files :: files containing additional metadata
        self.__metadata_files = []

        # self.__epub_cover_image :: epub cover image file name
        self.__epub_cover_image = str()

        # self.__metadata_new :: newly generated metadata
        self.__metadata_new = dict()

        # self.__input_dir :: directory of first input file
        input_fp = self.__json_msg['options']['pandoc']['input'][0]
        self.__input_dir = os.path.split(input_fp)[0]

        # self.__input_base :: basename of first input file
        self.__input_base = os.path.splitext(os.path.split(input_fp)[1])[0]

    def epub_cover_add(self):
        """ Add cover image to ast metadata
        """
        # build new metadata with cover image filepath
        new_entries = dict()
        new_entries['cover-image'] = self.__epub_cover_image
        yaml_meta = '\n---\n' + yaml.dump(new_entries) + '...\n\n'
        new_metadata = md_to_meta(yaml_meta)
        log('DEBUG', 'new metadata:')
        log_pretty_json(new_metadata)
        # add new metadata to ast
        self.__metadata_new = new_metadata
        self.__update_ast_with_new_metadata()

    def epub_cover_local(self):
        """ Find local image file to use as epub cover
            Returns: file name or None (updates self.__epub_cover_image)

            A valid epub image file is in the same directory as the
            (markdown) input file, i.e., current working directory,
            has the same basename as the input file, and has a
            'png', 'gif' or 'jpg' extension.

            If there are multiple matching image files, prefer
            png > gif > jpg.
        """
        cover_image = image_file(self.__input_dir, self.__input_base)
        if cover_image:
            self.__epub_cover_image = cover_image
        return cover_image

    def epub_cover_set(self):
        """ Whether cover image set on command line or in metadata
            Returns: 'in metadata'|'on the command line'|None

            If the cover image is specified in metadata the file path
            will be located in the JSON_MESSAGE like so:

                JSON_MESSAGE = {
                  ...,
                  'metadata': {
                    'cover-image': {
                      'c': [
                        {
                          'c': COVER_IMAGE_FILEPATH
                }]}}}

            If the cover image is specified on the command line the
            file path will be located in the JSON_MESSAGE like so:

                JSON_MESSAGE = {
                  ...,
                  'options': {
                    'pandoc': {
                      'options': {
                        'w': {
                          WRITE_OPTIONS
                }}}}}

            Only the first match is returned. The command line is
            examined first, so if a cover image is specified both
            on the command line and in metadata, the command line
            takes precedence.
        """
        # look in metadata
        if 'cover-image' in self.__json_msg['metadata']:
            if self.__json_msg['metadata']['cover-image']['c'][0]['c']:
                return 'in metadata'
        # look in command line
        write_options = self.__json_msg['options']['pandoc']['options']['w']
        if 'epub-cover-image' in write_options:  # can be 'None'
            if write_options['epub-cover-image']:
                return 'on the command line'
        # not set in either command line or metadata
        return None

    def load_extra_metadata(self):
        """ Loads metadata from metadata files
            Returns: void (updates self.__meta and self.__ast)

            Performs the following tasks:
            - get list of defined metadata filepaths
            - read data from metadata files
            - update ast
        """
        self.__locate_metadata_files()
        self.__read_metadata_files()
        if self.__metadata_new:
            self.__update_ast_with_new_metadata()
            log('DEBUG', 'updated ast with extra metadata')
        else:
            log('DEBUG', 'no extra metadata from reading metadata files')

    def write(self):
        """ Write pandoc abstract syntax tree to stdout
            Returns: void
        """
        log('DEBUG', 'writing ast')
        sys.stdout.write(json.dumps(self.__ast))
        sys.stdout.flush()

    @staticmethod
    def __extract_element_filenames(elements):
        """ Extract filenames from json elements
            Returns: list of filenames

            Assumes all elements have one of the following
            structures:

                {
                    't': 'MetaInlines',
                    'c': [
                        {
                            't': 'Str',
                            'c': 'file1.py'
                        }
                    ]
                }

                {
                    't': 'MetaInlines',
                    'c': [
                        {
                            't': 'Code',
                            'c': [
                              ['', [], []],
                              'file2.py'
                            ]
                        }
                    ],
                }

            It can be seen that each element defines a single file.
            (Note: in the original data where multiple files are
            defined in a single list, the resulting json data
            includes all list files in a list structure. This must
            be decomposed before using this function.)

            The two structures depend on whether the file name has
            type 'Str' (resulting if original file name was naked
            or enclosed in quotes) or type 'Code' (resulting if
            original file name was enclosed in quoted backticks).
        """
        filenames = []
        for element in elements:
            if element['t'] != 'MetaInlines':
                log('ERROR', 'invalid element: ' + str(element))
                raise ValueError('Expected MetaInlines, got ' + element['t'])
            entry = element['c'][0]
            entry_type = entry['t']
            entry_content = entry['c']
            if entry_type not in ['Str', 'Code']:
                log('ERROR', 'invalid element: ' + str(element))
                raise ValueError('Expected Str or Code, got ' + entry_type)
            if entry_type == 'Str':
                filename = entry_content
            else:  # must be 'Code' because above ensured no other values
                filename = entry_content[1]
            if filename not in filenames:
                filenames.append(filename)
        return filenames

    @staticmethod
    def __find_metadata_filepaths(filenames):
        """ Get filepaths for defined metadata files
            Returns: list of filepaths

            For each filename, try three possibilities in turn,
            accepting the first to return an existing match:
            1. The raw filename (which could actually be a filepath)
            2. The file is in the current working directory
            3. The file is in $HOME/.config/panzer/custom/
            4. The file is in $HOME/.panzer/custom/

            If no match is found, log a debug message.
        """
        cwd = os.getcwd()
        custom_default = os.path.join(os.environ['HOME'], '.panzer', 'custom')
        custom_config = os.path.join(os.environ['HOME'], '.config', 'panzer',
                                     'custom')
        filepaths = []
        for candidate in filenames:
            cwd_fp = os.path.join(cwd, os.path.basename(candidate))
            custom_default_fp = os.path.join(custom_default,
                                             os.path.basename(candidate))
            custom_config_fp = os.path.join(custom_config,
                                            os.path.basename(candidate))
            for fpath in [candidate, cwd_fp, custom_config_fp,
                          custom_default_fp]:
                if os.path.exists(fpath):
                    filepaths.append(fpath)
                    break
            else:
                log('INFO', '** cannot locate: ' + candidate)
        return filepaths

    def __locate_metadata_files(self):
        """ Get filepaths of defined metadata files
            Returns: void (updates self.__metadata_files)

            First, obtain json elements from ast defining metadata
            defining metadata file names, then extract the file
            names from the elements, and finally convert into
            file paths to existing files.
        """
        elements = self.__metadata_file_elements()
        if not elements:
            log('DEBUG', 'no json metadata file elements located')
            return

        filenames = self.__extract_element_filenames(elements)
        if not filenames:
            log('DEBUG', 'no metadata filenames extracted')
            return

        filepaths = self.__find_metadata_filepaths(filenames)
        if not filenames:
            log('DEBUG', 'no metadata filepaths confirmed')
            return

        for filepath in filepaths:
            if filepath not in self.__metadata_files:
                self.__metadata_files.append(filepath)

        if self.__metadata_files:
            msg = 'processing extra metadata file'
            if len(self.__metadata_files) > 1:
                msg += 's'
            msg += ':'
            log('INFO', msg)
            for filepath in self.__metadata_files:
                log('INFO', '- ' + filepath)
        else:
            log('INFO', 'no extra metadata files')

    def __metadata_file_elements(self):
        """ Get list of json elements defining metadata files
            Returns: list of json dict elements

            Metadata files can be defined in the input markdown file or
            the panzer style file.

            Metadata files defined in the input markdown file are found
            in the panzer-provided JSON_MESSAGE at:

                metadata: {
                  metadata-file: {>>HERE<<}
                }

            Metadata files defined in the panzer style file are found at:

                styledef: {
                  'STYLENAME1': {
                    't': 'MetaMap',
                    'c': {
                      'FORMAT1': {
                        't': 'MetaMap',
                        'c': {
                          'metadata': {
                            't': 'MetaMap',
                            'c': {
                            'metadata-file': {>>HERE<<}
                            }
                          }
                        }
                      },
                      'FORMAT2': {},
                    }
                  },
                  'STYLENAME2': {},
                }

            The metadata-file dictionary element values have two values,
            depending on whether they are defined in the source (md input
            file or panzer style file) as inline or a list.

            An inline metadata element has the structure:

                'metadata-file': {
                    't': 'MetaInlines',
                    'c': [
                        {
                            't': 'Str',
                            'c': 'file.py'
                        }
                    ]
                }

            A list metadata element has the structure:

                'metadata-file': {
                    't': 'MetaList',
                    'c': [
                        {
                            't': 'MetaInlines',
                            'c': [
                                {
                                    't': 'Str',
                                    'c': 'file1.py'
                                }
                            ],
                        },
                        {
                            't': 'MetaInlines',
                            'c': [
                                {
                                    't': 'Code',
                                    'c': [
                                      ['', [], []],
                                      'file2.py'
                                    ]
                                }
                            ],
                        }
                    ],
                },
            }
        """
        extracted = []
        # look in the metadata from the panzer style file
        if 'styledef' in self.__json_msg:
            styles = self.__json_msg['styledef']
            for style in styles:
                output_formats = styles[style]['c']
                for output_format in output_formats:
                    try:
                        extracted.append(output_formats[output_format]
                                         ['c']['metadata']
                                         ['c']['metadata-file'])
                    except KeyError:
                        pass
        # look in the metadata from the input markdown file
        if 'metadata' in self.__json_msg:
            if 'metadata-file' in self.__json_msg['metadata']:
                extracted.append(self.__json_msg['metadata']['metadata-file'])
        # all file entries are of type 'MetaInlines',
        # but if defined orginally in a list, then are wrapped in
        # a 'MetaList' structure, so have to flatten the list
        elements = []
        for extracted_element in extracted:
            if extracted_element['t'] == 'MetaList':
                elements.extend(extracted_element['c'])
            else:
                elements.append(extracted_element)
        return elements

    def __read_metadata_files(self):
        """ Uses pandoc to extract metadata files content
            Returns: void (updates self.__metadata_new)

            Where keys are defined in multiple metadata files,
            each time a key is redefined its value overwrites
            the earlier value. The key 'header-includes' is
            treated differently: its contents are harvested
            while processing the metadata files and all values
            written back to the metadata after all files are
            read
        """
        new_metadata = dict()
        metadata = dict()
        content = str()
        headers = list()
        for filepath in self.__metadata_files:
            with open(filepath, 'r') as md_file:
                content = md_file.read()
                new_metadata = md_to_meta(content)
                if 'header-includes' in new_metadata:
                    headers += new_metadata['header-includes']['c']
                metadata.update(new_metadata)
        if metadata:
            metadata['header-includes']['c'] = headers
            log('DEBUG', 'extracted metadata:')
            log_pretty_json(metadata)
        else:
            log('DEBUG', 'no metadata extracted')
        self.__metadata_new.update(metadata)

    def __update_ast_with_new_metadata(self):
        """ Integrate new metadata into ast
            Returns: void (updates self.__meta and self.__ast)
        """
        if not self.__metadata_new:
            log('DEBUG', 'no new metadata with which to update')
            return
        self.__meta.update(self.__metadata_new)
        self.__ast['meta'] = self.__meta
        self.__metadata_new = dict()


def md_to_meta(markdown):
    """ Extract meta content from markdown
        Returns: json dict

        Uses pandoc to convert markdown to a json abstract syntax
        tree (ast) and return the 'meta' value.
    """
    command = ['pandoc', '-',
               '--from', 'markdown',
               '--to', 'json',
               '--standalone']
    process = subprocess.Popen(command,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    stdin_bytes = markdown.encode(ENCODING)
    stdout_bytes = process.communicate(input=stdin_bytes)[0]
    stdout = stdout_bytes.decode(ENCODING)
    json_ast = json.loads(stdout)
    return json_ast['meta']


def log(level, message):
    """ Add message to panzer log file
    """
    outgoing = {'level': level, 'message': message}
    outgoing_json = json.dumps(outgoing) + '\n'
    outgoing_bytes = outgoing_json.encode(ENCODING)
    # pylint: disable=no-member
    sys.stderr.buffer.write(outgoing_bytes)
    sys.stderr.flush()


def get_keys(dict_var):
    """ Recursively obtain dictionary keys

    Stops descending when reaches a non-dictionary value,
    so some dictionary keys in a complex variable may be
    'hidden' from this function.
    """
    output = []
    keys = dict_var.keys()
    for key in keys:
        output.append(key)
        if isinstance(dict_var[key], dict):
            output.append(get_keys(dict_var[key]))
    return output


def which(program):
    """ Get path of executable
    """
    def is_exe(fpath):
        """ Determine whether filepath exists
        """
        return os.path.exists(fpath) \
            and os.access(fpath, os.X_OK) \
            and os.path.isfile(fpath)

    def ext_candidates(fpath):
        """ Add extensions that are used for executable files
        """
        yield fpath
        for ext in os.environ.get('PATHEXT', '').split(os.pathsep):
            yield fpath + ext

    fpath = os.path.split(program)[0]

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate

    return None


def image_file(fp_dir, fp_base):
    """ Find png, gif or jpg image file
        File will have given basename and be located in given directory.
        If multiple candidates present, prefer png > gif > jpg.
    """
    extensions = ['png', 'gif', 'jpg']
    for ext in extensions:  # look for file with image file extension
        candidate = os.path.join(fp_dir, fp_base + '.' + ext)
        if os.path.lexists(candidate):  # found image file!
            return candidate
    return None


def log_pretty_json(data):
    """ Pretty print a json variable
    """
    for line in pprint.pformat(data, width=60).splitlines():
        log('DEBUG', line)


# vim:fdm=indent:
