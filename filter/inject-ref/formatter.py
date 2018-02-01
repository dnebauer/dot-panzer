from pandocinject import Formatter

#####################################
#  block formatters for <div> tags  #
#####################################


class Base(Formatter):
    """docstring stub"""

    def sort_entries(self, entries):
        """docstring stub"""
        return entries
        # return sorted(entries, key=lambda x: custom_sort(x), reverse=True)


class APA_block(Base):
    """docstring stub"""

    def format_entry(self, entry):
        """docstring stub"""
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + entry.get('title', 'No title!'))
        # return(entry.get('title', 'No title!'))
        from style import apalike
        format = getattr(apalike, entry['ENTRYTYPE'], apalike.default)
        return format(entry)

    def format_block(self, entries, starred):
        """
        format a block containing entries
        """
        out = str()
        for entry in entries:
            # add each entry in loose numbered list
            out += '1.  '
            # star start of item
            if entry in starred:
                out += '\* '
            out += self.format_entry(entry)
            out += '\n'
        return out


class APA_inline(APA_block):
    """docstring stub"""

    def format_block(self, entries, starred):
        """
        format a block containing entries
        """
        out = str()
        for loop, entry in enumerate(entries):
            if entry in starred:
                out += '\* '
            out += self.format_entry(entry)
            if loop < len(entries)-1 and len(entries) > 1:
                out += '; '
        return out
