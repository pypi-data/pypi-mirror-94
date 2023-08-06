from ..Elements import Elements
from .Table import Table


class Tables(Elements):
    def __init__(self, parent_service_url):
        """Initialize and build our list of tables

        :param parent_service_url: url (unique) for the service containing all the tables
        """
        super().__init__()

        self.service_url = parent_service_url

    def _update(self):
        """Update list to be consistent with database"""
        self._elements = {}
        service_def_url = self.url_manager.resource_definition_url(self.service_url)
        service_def = self.request.get_in_python(service_def_url)
        for table in service_def['definition']['tables']:
            if 'isManaged' in service_def['definition']:
                is_managed = service_def['definition']['isManaged']
            else:
                is_managed = False
            self._elements[table['name']] = Table(table, self.service_url,
                                                  is_managed)

    def get_with_id(self, table_id):
        """Returns a table given its id
        """
        self._update()
        table_id = table_id.strip()
        for key, table in self._elements.items():
            if table.id == table_id:
                return table
        print("[WARNING] id", table_id, "doesn't exist, None is returned")
        return None
