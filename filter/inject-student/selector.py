from pandocinject import Selector

"""docstring stub"""


# pylint: disable=no-self-use
class Primary(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('kind', '-1') == 'primary':
            return True
        return False


# pylint: disable=no-self-use
class Secondary(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if entry.get('kind', '-1') == 'secondary':
            return True
        return False


# pylint: disable=no-self-use
class Current(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if not entry['degree'].get('completed', False):
            return True
        return False


# pylint: disable=no-self-use
class Past(Selector):
    """docstring stub"""
    def select(self, entry):
        """docstring stub"""
        if not entry['degree'].get('completed', False):
            return False
        return True
