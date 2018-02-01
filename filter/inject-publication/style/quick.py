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
            output += ', *%s*' % entry['published']['journal']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
        else:
            output += ' (%s)' % entry['status']
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
    output += ', '
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
        else:
            output += ' (%s)' % entry['status']
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
    output += ', '
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
        else:
            output += ' (%s)' % entry['status']
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
    output += ', '
    try:
        if entry['published']['journal']:
            output += '*%s*' % entry['published']['journal']
    except KeyError:
        pass
    try:
        if entry['published']['year']:
            output += ' (%s)' % str(entry['published']['year'])
        else:
            output += ' (%s)' % entry['status']
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
    output += ', '
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
        else:
            output += ' (%s)' % entry['status']
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
              if a['name_last'] != 'Nebauer' and a['name_first'] != 'David']
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
              if a['name_last'] != 'Nebauer' and a['name_first'] != 'David']
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


def concat(items, sep, final_sep):
    """docstring stub"""
    output = str()
    if not items:
        return output
    output += items[0]['name_first'] + ' ' + items[0]['name_last']
    if len(items) == 1:
        return output
    for i in range(1, len(items) - 1):
        output += sep
        output += items[i]['name_first'] + ' ' + items[i]['name_last']
    output += final_sep
    output += items[-1]['name_first'] + ' ' + items[-1]['name_last']
    return output


def concat_useinitials(items, sep, final_sep):
    """docstring stub"""
    output = str()
    # no one in list
    if not items:
        return output
    # first person in list
    output += name2initials(items[0]['name_first'])
    output += ' '
    output += items[0]['name_last']
    if len(items) == 1:
        return output
    # everyone else until penultimate person
    for i in range(1, len(items) - 1):
        output += sep
        output += name2initials(items[i]['name_first'])
        output += ' '
        output += items[i]['name_last']
    # last person in list
    output += final_sep
    output += name2initials(items[-1]['name_first'])
    output += ' '
    output += items[-1]['name_last']
    return output


def add_note(entry):
    """docstring stub"""
    output = str()
    if 'published' in entry and 'note' in entry['published'] and \
            entry['published']['note']:
        output += ' (%s)' % entry['published']['note']
    return output


def add_urls(entry):
    """docstring stub"""
    output = str()
    return output
