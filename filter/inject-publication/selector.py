from pandocinject import Selector

##########################
#  Status of publication #
##########################


class Proposed(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('status', 'x') == 'proposed':
            return True
        return False


class InPreparation(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('status', 'x') == 'in preparation':
            return True
        return False


class UnderReview(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('status', 'x') == 'under review':
            return True
        return False


class Forthcoming(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('status', 'x') == 'forthcoming':
            return True
        return False


class Published(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('status', 'x') == 'published':
            return True
        return False


##########################
#  Types of publication  #
##########################


class Monograph(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['monograph']:
            return True
        return False


class EditedCollection(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['editedcollection']:
            return True
        return False


class SpecialIssue(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['specialissue']:
            return True
        return False


class Article(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['article']:
            return True
        return False


class BookReview(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['bookreview']:
            return True
        return False


class InCollection(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['incollection']:
            return True
        return False


class Misc(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if 'published' in entry and entry['published'].get('type', 'x') \
                in ['misc']:
            return True
        return False


################
#  Authorship  #
################


class SingleAuthor(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if len(entry.get('author', ['x'])) == 1:
            return True
        return False
