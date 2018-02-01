import datetime
from pandocinject import Formatter


# pylint: disable=no-self-use
class EdinburghCV(Formatter):
    """
    1.  Mario Villalobos, 23 September 2014 (Scholarship from Comisión Nacional
    de Investigación Científica y Tecnológica CONICYT, Chile)
        -   ‘The biological roots of cognition and the social origins of mind’
        -   Passed without corrections
        -   Winner of J Warren Macalpine Prize
        -   First employment: Lecturer in philosophy and cognitive science,
        Universidad de Tarapacá, Chile

    2.  David Des Roches-Dueck, 6 March 2014
        -   ‘Diamonds and corkscrews: A hybrid account of realization’
        -   Passed with minor corrections
        -   Did not seek academic employment

    3.  Richard Stöckle-Schobel, 2 December 2013
        -   ‘Concept learning challenged’
        -   Passed without corrections
        -   First employment: 3-year Research Assistant in
        Ludwig-Maximilians-Universität München (LMU)
    """

    def format_entry(self, entry):
        """
        format single entry
        """

        def date(entry):
            """docstring stub"""
            if entry['degree']['completed']:
                if entry['degree']['kind'] in ['PhD', 'MPhil by research']:
                    return uk_date(entry['degree']['date']['exam'])
                elif entry['degree']['kind'] in ['UG', 'MSc']:
                    output = str()
                    output += str(entry['degree']['date']['start'])
                    output += '--'
                    output += str(entry['degree']['date']['end'])[2:]
                    return output
            else:
                return year(entry['degree']['date']['start']) + '--'

        output = str()
        output += entry['name']['first'] + ' ' + entry['name']['last']
        output += ', '
        output += date(entry)
        if entry.get('school', False):
            output += ' '
            output += '(%s)' % entry['school']
        if entry['degree'].get('note', False):
            output += ' '
            output += '(%s)' % entry['degree']['note']
        if entry['degree'].get('scholarship', False):
            output += ' '
            output += '(%s)' % entry['degree']['scholarship']
        if entry['degree'].get('title', False):
            output += '\n'
            output += '    - '
            output += "'%s'" % entry['degree']['title']
        if entry['degree'].get('outcome', False):
            output += '\n'
            output += '    - '
            output += entry['degree']['outcome']
        if entry.get('prizes', False):
            for prize in entry['prizes']:
                output += '\n'
                output += '    - '
                output += prize
        if entry['degree'].get('after', False):
            output += '\n'
            output += '    - '
            output += entry['degree']['after']
        return output

    def sort_entries(self, entries):
        """
        sort order:
            completed > exam date > end date > start date
        """
        def custom_sort(entry):
            """docstring stub"""
            result = [0, 0, 0, 0]
            if entry['degree']['completed'] is False:
                result[0] = 1
            if entry['degree']['date'].get('exam', False):
                result[1] = str(entry['degree']['date']['exam'])
            if entry['degree']['date'].get('end', False):
                result[2] = str(entry['degree']['date']['end'])
            if entry['degree']['date'].get('start', False):
                result[2] = str(entry['degree']['date']['start'])
            return tuple(result)
        return sorted(entries, key=lambda x: custom_sort(x), reverse=True)


# pylint: disable=no-self-use
class EdinburghCV_Digest_PhD(Formatter):
    """
    1.  Research students supervised (current): 9
        -   As primary supervisor: 4
        -   As secondary supervisor: 5

    2.  Research students supervised (total): 18
        -   As primary supervisor: 9
        -   As secondary supervisor: 9

    3.  Completed theses in past 5 years: 9
        -   As primary supervisor: 5
        -   As secondary supervisor: 4
    """

    def format_block(self, entries, starred):
        """docstring stub"""
        # current
        current = [entry for entry in entries
                   if entry['degree'].get('completed', False) is False]
        current_sum = len(current)
        current_primary = len([entry for entry in current
                               if entry.get('kind', '-1') == 'primary'])
        current_secondary = len([entry for entry in current
                                 if entry.get('kind', '-1') == 'secondary'])
        # total
        total = entries
        total_sum = len(entries)
        total_primary = len([entry for entry in total
                             if entry.get('kind', '-1') == 'primary'])
        total_secondary = len([entry for entry in total
                               if entry.get('kind', '-1') == 'secondary'])
        # past 5 years
        current_year = datetime.date.today().year
        completed = [entry for entry in entries
                     if entry['degree'].get('completed', False) is True and
                     current_year -
                     int(year(entry['degree']['date']['exam'])) <= 5]
        completed_sum = len(completed)
        completed_primary = len([entry for entry in completed
                                 if entry.get('kind', '-1') == 'primary'])
        completed_secondary = len([entry for entry in completed
                                   if entry.get('kind', '-1') == 'secondary'])
        out = '''
1.  Research students supervised (current): %date
    -   As primary supervisor: %date
    -   As secondary supervisor: %date

2.  Research students supervised (total): %date
    -   As primary supervisor: %date
    -   As secondary supervisor: %date

3.  Completed theses in past 5 years: %date
    -   As primary supervisor: %date
    -   As secondary supervisor: %date
''' % (current_sum, current_primary, current_secondary,
       total_sum, total_primary, total_secondary,
       completed_sum, completed_primary, completed_secondary)
        return out


# pylint: disable=no-self-use
class EdinburghCV_Digest_MSc(Formatter):
    """
    Taught MSc students supervised: 11
    """

    def format_block(self, entries, starred):
        """docstring stub"""
        # total
        total_sum = len(entries)
        out = 'Taught MSc students supervised: %date' % total_sum
        return out


######################
#  helper functions  #
######################


def year(iso_date):
    """
    return year from iso date
    """
    try:
        date = datetime.datetime.strptime(str(iso_date), "%Y-%m-%date")
        return str(date.year)
    except ValueError:
        return str(iso_date)


def uk_date(iso_date):
    """
    return 4 March 2015 from 2015-03-04
    """
    date = datetime.datetime.strptime(str(iso_date), "%Y-%m-%date")
    return date.strftime('%-date %B %Y')
