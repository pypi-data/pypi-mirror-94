from .Fields import Fields
from .Resource import Resource


class Table(Resource):
    def __init__(self, description, parent_service_url, is_managed=False):
        super().__init__(parent_service_url + "/" + str(description['id']),
                         parent_access = parent_service_url, is_managed = is_managed)
        self.id = str(description['id'])
        self.name = description['name']

        self._fields = Fields(self.parent_access, self.id)

    @property
    def fields(self):
        """
        :return: List of fields corresponding to this layer
        """
        return self._fields

    def _can_activate_FDU(self, group_rights, filt, group):
        """Verify if can apply a given filter to this table
        Only possible if filter's attributes are in table's fields.

        :param group_rights: Contains current rights on this table
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not super()._can_activate_FDU(group_rights, filt, group):
            return False
        for attr in filt.get_fields():
            if self.fields.get(attr) is None:
                print('In order to apply filter on a table, its attributes has to be in fields')
                return False
        return True

    @staticmethod
    def get_type():
        return "TABLE"

    def __str__(self):
        return 'Table {}; name {}; for Service {}'.format(self.id, self.name, self.parent_access)
