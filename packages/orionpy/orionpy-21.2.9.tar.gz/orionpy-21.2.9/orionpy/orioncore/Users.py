# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
from .Subjects import Subjects
from .User import User


class Users(Subjects):
    """
    Class allowing to get access to the defined users

    """

    def __init__(self):
        super().__init__('users', 'username', 'fullName')

    def _get_system_subject_id(self):
        return []

    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        return User(subject_title, subject_id + "(agol)", profile_id)

    def get_with_id(self, subject_id):
        if not subject_id.endswith('(agol)'):
            subject_id = subject_id + "(agol)"
        return super(Users, self).get_with_id(subject_id)