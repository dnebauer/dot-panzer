"""docstring stub"""


def default(entry):
    """docstring stub"""
    # get the data
    author = author_or_editor(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def article(entry):
    """docstring stub"""
    # get the data
    author = author_or_editor(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    journal = myget(entry, 'journal', '=no journal=')
    volume = myget(entry, 'volume', None)
    pages = myget(entry, 'pages', None)
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += '*%s*' % journal
    if volume:
        text += ' '
        text += volume
    if pages:
        text += ', '
        text += ' ' + pages
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def unpublished(entry):
    """docstring stub"""
    # get the data
    author = author_or_editor(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += 'unpublished manuscript'
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def phdthesis(entry):
    """docstring stub"""
    # get the data
    author = author_or_editor(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    school = myget(entry, 'school', '=no school=')
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += school
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def mastersthesis(entry):
    """docstring stub"""
    return phdthesis(entry)


def book(entry):
    """docstring stub"""
    # get the data
    author = author_or_editor(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    publisher = myget(entry, 'publisher', None)
    address = myget(entry, 'address', None)
    edition = myget(entry, 'edition', None)
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += '*%s*' % title
    if address or publisher:
        text += ', '
        if address:
            text += address
            text += ': '
        if publisher:
            text += publisher
    if edition:
        text += ', '
        if edition == '1':
            text += '1st'
        if edition == '2':
            text += '2nd'
        if edition == '3':
            text += '3rd'
        else:
            text += '%sth' % edition
        text += ' Edition'
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def incollection(entry):
    """docstring stub"""
    # get the data
    author = author(entry, 5)
    year = myget(entry, 'year', 'no year')
    title = myget(entry, 'title', '=no title=')
    publisher = myget(entry, 'publisher', None)
    address = myget(entry, 'address', None)
    editor = editor(entry, 3)
    pages = myget(entry, 'pages', None)
    booktitle = myget(entry, 'booktitle', '=no booktitle=')
    bibtex_key = entry['ID']
    bibtex_type = entry['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += '%s' % title
    if editor != '=no editor=' or booktitle != '=no booktitle=':
        text += ' in'
        if editor != '=no editor=':
            text += ' '
            text += editor
            text += ' '
            if len(entry['editor']) == 1:
                text += '(Ed.)'
            else:
                text += '(Eds.)'
        text += ' '
        text += '*%s*' % booktitle
    if address or publisher:
        text += ', '
        if address:
            text += address
            text += ': '
        if publisher:
            text += publisher
    if pages:
        text += ', '
        text += 'pp. ' + pages
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text


def inproceedings(entry):
    """docstring stub"""
    return incollection(entry)


def inbook(entry):
    """docstring stub"""
    return incollection(entry)


def myget(entry, key, default):
    """
    return entry.get(key, default)
    if bibtex version of key not found, use biblatex version
    """
    biblatex = {'year': 'date',
                'journal': 'journaltitle',
                'address': 'location'}
    if key not in biblatex:
        return entry.get(key, default)
    return entry.get(key, entry.get(biblatex[key], default))


def author_or_editor(entry, max_num):
    """
    return string flattened list of either authors or editors
    - authors returned in preference to editors
    - if neither found, then '=no author=' is returned
    :entry: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with authors or editors
    """
    authors = myget(entry, 'author', None)
    editors = myget(entry, 'editor', None)
    if authors:
        return flatten_list(authors, max_num)
    if editors:
        return flatten_list(editors, max_num)
    return '=no author='


def author(entry, max_num):
    """
    return string flattened list of authors
    - if not found, then '=no author=' is returned
    :entry: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with authors
    """
    authors = myget(entry, 'author', ['=no author='])
    return flatten_list(authors, max_num)


def editor(entry, max_num):
    """
    return string flattened list of editors
    - if not found, then '=no author=' is returned
    :entry: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with editors
    """
    editors = myget(entry, 'editor', ['=no editor='])
    return flatten_list(editors, max_num)


def flatten_list(names, max_num):
    """
    flattens a list of authors or editors and caps it a max number
    :names: list of names
    :num: maximum number of names to include, others marked by 'et al.'
    :returns: string of flattened list
    """
    # sanity check: empty list returns empty string
    if not names:
        return ''
    # add first author
    text = names[0]
    # add next authors
    for i in range(1, min(max_num, len(names))):
        text += ' and ' + names[i]
    # add truncated authors
    if len(names) > max_num:
        text += ' et al.'
    return text


def remove_latex_crap(incoming):
    """
    remove funny latex characters and text from incoming string
    - uses list of subs for find and replace
    :returns: string with characters removed
    """
    subs = [('~', ' '),
            ('\\emph{', ''),
            ('}', ''),
            ('{', ''),
            ('\\', ''),
            ('--', '-')]
    text = incoming
    for s in subs:
        text = text.replace(s[0], s[1])
    return text
