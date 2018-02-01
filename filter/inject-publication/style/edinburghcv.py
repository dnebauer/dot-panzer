#######################
#  default formatter  #
#######################


def default(entry):
    """docstring stub"""
    output = str()
    output += entry['title']
    output += '  -- WARNING: default formatter activated!'
    return output


###########################################
#  formmatters for each publication type  #
###########################################


def article(entry):
    """docstring stub"""
    output = str()
    output += "'%s'" % entry['title']
    output += add_coauthors(entry)
    try:
        if entry['published']['journal']:
            output += '\\' + '\n'
            output += '*%s*' % entry['published']['journal']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
    except KeyError:
        pass
    try:
        if entry['published']['volume']:
            output += ' %s' % str(entry['published']['volume'])
    except KeyError:
        pass
    try:
        if entry['published']['pages']:
            output += ', %s' % entry['published']['pages']
    except KeyError:
        pass
    output += add_note(entry)
    output += add_urls(entry)
    return output


def bookreview(entry):
    """docstring stub"""
    return article(entry)


def monograph(entry):
    """docstring stub"""
    output = str()
    output += "*%s*" % entry['title']
    output += add_coauthors(entry)
    output += '\\' + '\n'
    try:
        if entry['published']['publisher']:
            output += '%s' % entry['published']['publisher']
    except KeyError:
        pass
    try:
        if entry['published']['address']:
            output += ': %s' % entry['published']['address']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
    except KeyError:
        pass
    try:
        if entry['published']['length']:
            output += ', %s' % entry['published']['length']
    except KeyError:
        pass
    output += add_note(entry)
    output += add_urls(entry)
    return output


def editedcollection(entry):
    """docstring stub"""
    output = str()
    output += "*%s*" % entry['title']
    output += add_coeditors(entry)
    output += '\\' + '\n'
    try:
        if entry['published']['publisher']:
            output += '%s' % entry['published']['publisher']
    except KeyError:
        pass
    try:
        if entry['published']['address']:
            output += ': %s' % entry['published']['address']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
    except KeyError:
        pass
    try:
        if entry['published']['length']:
            output += ', %s' % entry['published']['length']
    except KeyError:
        pass
    output += add_note(entry)
    output += add_urls(entry)
    return output


def specialissue(entry):
    """docstring stub"""
    output = str()
    output += "%s" % entry['title']
    output += add_coeditors(entry)
    output += '\\' + '\n'
    try:
        if entry['published']['journal']:
            output += '*%s*' % entry['published']['journal']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
    except KeyError:
        pass
    try:
        if entry['published']['length']:
            output += ', %s' % entry['published']['length']
    except KeyError:
        pass
    output += add_note(entry)
    output += add_urls(entry)
    return output


def incollection(entry):
    """docstring stub"""
    output = str()
    if 'title' in entry:
        output += "'%s'" % entry['title']
    elif 'description' in entry:
        output += "%s" % entry['description']
    output += add_coauthors(entry)
    output += '\\' + '\n'
    output += 'in '
    output += add_volumeeditors(entry)
    output += ' '
    try:
        if entry['published']['booktitle']:
            output += '*%s*' % entry['published']['booktitle']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
    except KeyError:
        pass
    try:
        if entry['published']['publisher']:
            output += ', %s' % entry['published']['publisher']
    except KeyError:
        pass
    try:
        if entry['published']['address']:
            output += ': %s' % entry['published']['address']
    except KeyError:
        pass
    try:
        if entry['published']['pages']:
            output += ', %s' % entry['published']['pages']
    except KeyError:
        pass
    output += add_note(entry)
    output += add_urls(entry)
    return output


def misc(entry):
    """docstring stub"""
    return incollection(entry)


######################
#  helper functions  #
######################


def add_coauthors(entry):
    """docstring stub"""
    output = str()
    if len(entry['author']) == 1:
        return output
    output += ' (with '
    a_list = [a
              for a in entry['author']
              if a['name_last'] != 'Sprevak' and a['name_first'] != 'Mark']
    output += concat(a_list, ', ', ' and ')
    output += ')'
    return output


def add_coeditors(entry):
    """docstring stub"""
    output = str()
    if len(entry['editor']) == 1:
        output += ' (Ed.)'
        return output
    output += ' (with '
    a_list = [a
              for a in entry['editor']
              if a['name_last'] != 'Sprevak' and a['name_first'] != 'Mark']
    output += concat(a_list, ', ', ' and ')
    output += ')'
    output += ' (Eds.)'
    return output


def add_volumeeditors(entry):
    """docstring stub"""
    output = str()
    try:
        if not entry['published']['editor']:
            return output
    except KeyError:
        return output
    output += concat_useinitials(entry['published']['editor'], ', ', ' and ')
    if len(entry['published']['editor']) > 1:
        output += ' (Eds.)'
    else:
        output += ' (Ed.)'
    return output


def name2initials(name):
    """docstring stub"""
    return ' '.join([n[0] + '.' for n in name.split()])


def concat(init_list, sep, final_sep):
    """docstring stub"""
    output = str()
    if not init_list:
        return output
    output += init_list[0]['name_first'] + ' ' + init_list[0]['name_last']
    if len(init_list) == 1:
        return output
    for i in range(1, len(init_list) - 1):
        output += sep
        output += init_list[i]['name_first'] + ' ' + init_list[i]['name_last']
    output += final_sep
    output += init_list[-1]['name_first'] + ' ' + init_list[-1]['name_last']
    return output


def concat_useinitials(init_list, sep, final_sep):
    """docstring stub"""
    output = str()
    # no one in list
    if not init_list:
        return output
    # first person in list
    output += name2initials(init_list[0]['name_first'])
    output += ' '
    output += init_list[0]['name_last']
    if len(init_list) == 1:
        return output
    # everyone else until penultimate person
    for i in range(1, len(init_list) - 1):
        output += sep
        output += name2initials(init_list[i]['name_first'])
        output += ' '
        output += init_list[i]['name_last']
    # last person in list
    output += final_sep
    output += name2initials(init_list[-1]['name_first'])
    output += ' '
    output += init_list[-1]['name_last']
    return output


def add_note(entry):
    """docstring stub"""
    output = str()
    if 'published' in entry and 'note' in entry['published'] \
            and entry['published']['note']:
        output += ' (%s)' % entry['published']['note']
    return output


def add_urls(entry):
    """docstring stub"""
    output = str()
    output += '\\' + '\n'
    try:
        if entry['deploy']['url']:
            output += '[[PDF]](%s)' % entry['deploy']['url']
    except KeyError:
        pass
    try:
        if entry['published']['doi']:
            output += ' '
            output += '[[DOI]](http://dx.doi.org/%s)' \
                % entry['published']['doi']
    except KeyError:
        pass
    try:
        for url in entry['published']['href']:
            output += ' '
            output += '[[%s]](%s)' % (url['title'], url['url'])
    except KeyError:
        pass
    return output
