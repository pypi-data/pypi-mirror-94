# https://front1051.arcopole.fr/Orion/orion/admin/tree/object/SERVICES/Cannes/EspacesVerts_FeatureServer/2
# {
# "nodeInformationData":"LAYER",
# "definition":
#  {
#   "id":$layer_id$,
#   "name":$layer_name$,
#
#   "fields":
#    [
#       {
#        "name":$field_name/id$,
#        "type":$field_type$,
#        "alias":$field_alias$,
#        "editable":false,
#        "nullable":false,
#         [length]: $len$,
#       },
#    ],
#   "restRelativeURL":"Cannes/EspacesVerts/FeatureServer/2",
#  }
# }

from enum import Enum

from .Field import Field
from ..Elements import Elements


class FieldsKeys(Enum):
    fields_key = 'fields'
    def_key = 'definition'


class Fields(Elements):
    """Class allowing to get access to a list of fields for a particular layer
    """

    # TODO : Fields can also be identified with there alias. Be able to get a field using this alias.
    # ==> Add a method get_with_alias

    def __init__(self, service_url, layer_id):
        super().__init__()
        self.parent_url = service_url
        self.layer_id = layer_id
        self.parent_access = service_url + "/" + layer_id

    def _update(self):
        """Make sure that list of fields is up to date"""
        self._elements = {}
        parent_def = self.request.get_in_python(
            self.url_manager.resource_definition_url(self.parent_access))
        if parent_def[FieldsKeys.def_key.value][FieldsKeys.fields_key.value] is None:
            return
        for field in parent_def[FieldsKeys.def_key.value][FieldsKeys.fields_key.value]:
            if 'isManaged' in parent_def[FieldsKeys.def_key.value]:
                is_managed = parent_def[FieldsKeys.def_key.value]['isManaged']
            else:
                is_managed = False
            self._elements[field['name']] = Field(field, self.parent_url, self.layer_id,
                                                  parent_def[FieldsKeys.def_key.value]['capabilities'],
                                                  is_managed)
