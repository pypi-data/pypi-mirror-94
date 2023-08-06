import abc

from .RequestManager import RequestManager
from .UrlBuilder import UrlBuilder


class Elements(metaclass = abc.ABCMeta):
    # TODO Add a "search" method ?
    """Interface for classes containing a list of elements.

    Attributes:
        _elements : Dictionary containing elements
    """

    def __init__(self):
        self._elements = {}
        self.url_manager = UrlBuilder()
        self.request = RequestManager()

    @abc.abstractmethod
    def _update(self):
        """Updates elements for it to be consistent with database"""
        raise NotImplementedError('class must define _update() to use this base class')

    def _update_one(self, element_id):
        """Updates one element for it to be consistent with database"""
        return None

    def all(self):
        """
        :return: the list of elements' values sorted case-insensitive by their name
        """
        self._update()
        return sorted(self._elements.values(), key = lambda elem: elem.name.lower())

    def get(self, element_name):
        """Look for a particular element in elements.

        :param element_name: identification of element
        :return: required element or None if nothing found
        """
        # If possible and useful, call update_one instead !
        self._update()
        element_name = element_name.strip()
        if element_name in self._elements:
            return self._elements[element_name]
        print("[WARNING] element", element_name, "doesn't exist, None is returned")
        return None
