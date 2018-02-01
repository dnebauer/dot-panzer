from pandocinject import Formatter

#####################################
#  block formatters for <div> tags  #
#####################################


class Base(Formatter):
    """docstring stub"""

    def sort_entries(self, entries):
        """docstring stub"""
        def custom_sort(entry):
            """docstring stub"""
            rank = [0, 0]
            # 1. sort by status
            # - 'in preparation' comes first
            # - 'under review' comes first
            # - 'forthcoming' comes next
            if entry['status'] == 'proposed':
                rank[0] = 6
            elif entry['status'] == 'in preparation':
                rank[0] = 5
            elif entry['status'] == 'under review':
                rank[0] = 4
            elif entry['status'] == 'forthcoming':
                rank[0] = 3
            elif entry['status'] == 'published':
                rank[0] = 2
            # 2. sort by date_updated
            rank[1] = entry['date_updated']
            # 3. sort by title/description
            atom = str()
            if 'title' in entry:
                atom = entry['title']
            elif 'description' in entry:
                atom = entry['description']
            return tuple(rank) + tuple(atom)
        return sorted(entries, key=lambda x: custom_sort(x), reverse=True)


class EdinburghCV(Base):
    """docstring stub"""

    def format_entry(self, entry):
        """docstring stub"""
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + entry.get('title', 'No title!'))
        from style import edinburghcv
        if 'published' in entry:
            nhig = entry['published']['type']
        else:
            nhig = 'default'
        fhig = getattr(edinburghcv, nhig, edinburghcv.default)
        return fhig(entry)

class Quick(Base):
    """docstring stub"""

    def format_entry(self, entry):
        """docstring stub"""
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + entry.get('title', 'No title!'))
        from style import quick
        if 'published' in entry:
            nhig = entry['published']['type']
        else:
            nhig = 'default'
        fhig = getattr(quick, nhig, quick.default)
        return fhig(entry)
