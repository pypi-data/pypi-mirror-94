# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
import abc

from .Elements import Elements
from .Subject import Subject


class Subjects(Elements):
    """
    Class allowing to get access to the defined groups

    """

    def __init__(self, subject_type, id_key, title_key):
        super().__init__()
        
        self.subject_type = subject_type
        self.title_key = title_key
        self.id_key = id_key


    @abc.abstractmethod
    def _get_system_subject_id(self):
        """Return list of subject id"""
        raise NotImplementedError('class must define _get_system_subject_id() to use this base class')

    def _update(self):
        """Make sure that list of elements is up to date with DB state.
        Name is the key to get a particular group
        """
        self._elements = {}
        next_start = 0

        # Get portal self description
        self_portal = self.request.get_in_python(self.url_manager.self_url())
        org_id = self_portal['id']

        while next_start != -1:
            next_start = self._search_subjects(org_id, next_start)

    def _search_subjects(self, org_id, next_start):
        """Look for a particular group in the list using its id

        :param org_id: org id of portal
        :param start: start value to request
        :return: next_start value. if value is -1 there is no more data
        """
        params = {'f': 'json'}
        params['q'] = '(orgid:{org_id} -owner:esri_livingatlas -owner:esri_boundaries -owner:esri_demographics -owner:esri_nav)'.format(org_id = org_id)
        params['num'] = 100
        params['start'] = next_start

        subject_structs = self.request.get_in_python(self.url_manager.subject_list_url(self.subject_type), params)

        for subject_struct in subject_structs["results"]:
            subject_id = subject_struct[self.id_key]
            subject_title = subject_struct.get(self.title_key) or subject_struct.get(self.id_key)

            self._elements[subject_title] = self._create_subject_instance(subject_title, subject_id, None)
        return subject_structs['nextStart']

    @abc.abstractmethod
    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        """Create instance of the specific subject"""
        raise NotImplementedError('class must define _create_subject_instance() to use this base class')

    def get_with_id(self, subject_id):
        """Look for a particular group in the list using its id

        :param group_id: id of the group to look for
        :return: the required group or None if nothing found
        """
        self._update()
        subject_id = subject_id.strip()
        for key, subject in self._elements.items():
            if subject.id == subject_id:
                return subject
        return None

    def all(self):
        """
        :return: the list of elements' values
        """
        # TODO convert to list ?
        self._update()
        return sorted(self._elements.values(),
                      key = lambda group: group.title.lower())
