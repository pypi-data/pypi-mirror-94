# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
from .Subjects import Subjects
from .Group import Group


class Groups(Subjects):
    """
    Class allowing to get access to the defined groups

    """

    def __init__(self):
        super().__init__('groups', 'id', 'title')
        self.name_key = 'name'

    def _get_system_subject_id(self):
        return ['org', 'public']

    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        return Group(subject_title, subject_id, profile_id)

    def _update(self):
        super(Groups, self)._update()
        # Groups 'organisation' and 'tout le monde' require a specific treatment
        for subject_id in self._get_system_subject_id():
            subject_url = self.url_manager.subject_information_url(self.subject_type, subject_id)
            subject_str = self.request.get_in_python(subject_url)
            profile_id = subject_str['properties']['builtinRole']
            subject_id = subject_str[self.name_key]
            subject_title = subject_str[self.title_key]

            self._elements[subject_title] = self._create_subject_instance(subject_title, subject_id, profile_id)