from util import there


#######################
#  default formatter  #
#######################


def default():
    """docstring stub"""
    output = '**WARNING**: default formatter activated!'
    return output


###########################################
#  formmatters for each publication type  #
###########################################


def article(entry):
    """docstring stub"""
    output = str()
    output += prefix(entry)
    info = entry['published']
    if there('journal', info):
        output += '*' + info['journal'] + '*'
        output += ' '
    if there('year', info):
        output += '(' + str(info['year']) + ')'
        output += ' '
    if there('volume', info):
        output += str(info['volume'])
        output += ': '
    if there('pages', info):
        output += info['pages']
    output = output.rstrip()
    return output


def incollection(entry):
    """docstring stub"""
    output = str()
    output += prefix(entry)
    info = entry['published']
    if there('editor', info):
        output += concat_useinitials(info['editor'], ', ', ' & ')
        output += ' '
        if len(info['editor']) > 1:
            output += '(Eds.)'
        else:
            output += '(Ed.)'
        output += ' '
    if there('booktitle', info):
        output += '*' + info['booktitle'] + '*'
    if there('year', info) and isinstance(info['year'], int):
        output += ' '
        output += '(' + str(info['year']) + ')'
    if there('address', info):
        output += ', '
        output += info['address']
        output += ': '
    if there('publisher', info):
        output += info['publisher']
    if there('pages', info):
        output += ', '
        output += 'pp. ' + info['pages']
    elif there('chapter', info):
        output += 'chapter ' + info['chapter']
    output = output.rstrip()
    output = output.rstrip(',')
    return output


def bookreview(entry):
    """docstring stub"""
    return article(entry)


######################
#  helper functions  #
######################


def name2initials(name):
    """docstring stub"""
    return ' '.join([n[0] + '.' for n in name.split()])


def concat_useinitials(inits, sep, final_sep):
    """docstring stub"""
    output = str()
    # no one in list
    if not inits:
        return output
    # first person in list
    output += name2initials(inits[0]['name_first'])
    output += ' '
    output += inits[0]['name_last']
    if len(inits) == 1:
        return output
    # everyone else until penultimate person
    for i in range(1, len(inits) - 1):
        output += sep
        output += name2initials(inits[i]['name_first'])
        output += ' '
        output += inits[i]['name_last']
    # last person in list
    output += final_sep
    output += name2initials(inits[-1]['name_first'])
    output += ' '
    output += inits[-1]['name_last']
    return output


def prefix(entry):
    """docstring stub"""
    if 'status' in entry:
        if entry['status'] == 'published':
            return 'Published in '
        elif entry['status'] == 'forthcoming':
            return 'Final version due to appear in '
        elif entry['status'] == 'in press':
            return 'In press with '
    return 'Final version due to appear in '
