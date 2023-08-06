# https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/profiles/authenticated/aobrights/SERVICES/SampleWorldCities_MapServer/__configure
# {"isInherited":false,"rights":[{"filteredDimensions":["32d0b429-452a-40bd-9865-5a6c6798007a"],"action":"read"}]}

# ---- Get layers corresponding to a service :
# https://front1051.arcopole.fr/Orion/orion/admin/tree/object/SERVICES/Cannes/EspacesVerts_FeatureServer
# f & token
# "definition":
# {
#     "layers":
#         [
#             {
#                 "id":$LAYER_ID$,
# "name":$LAYER_NAME$,
# "parentLayerId":$parentLayerId$,
# "defaultVisibility": bool,
# "subLayerIds": null,
# "minScale": 0,
# "maxScale": 0
# },
# ],

from ..Elements import Elements
from .Layer import Layer


class Layers(Elements):
    """
    Class allowing to get access to a list of Layers for a particular service
    """

    def __init__(self, parent_service_url):
        """Initialize and build our list of layers

        :param parent_service_url: url (unique) for the service containing all those layers
        """
        super().__init__()
        self.service_url = parent_service_url

    def _update(self):
        """Update list to be consistent with database
        """
        self._elements = {}
        service_def_url = self.url_manager.resource_definition_url(self.service_url)
        service_def = self.request.get_in_python(service_def_url)
        for layer in service_def['definition']['layers']:
            if 'isManaged' in service_def['definition']:
                is_managed = service_def['definition']['isManaged']
            else:
                is_managed = False
            self._elements[layer['id']] = Layer(layer, self.service_url,
                                                service_def['definition']['capabilities'],
                                                is_managed)

    def get_id(self, layer_name):
        """With the name of a layer, allows to get its id

        :param layer_name: Name of layer for which we want the id
        :return: Layer id or None if nothing was found
        """
        layer = self.get(layer_name)
        if layer is not None:
            return layer.id
        return None

    def get_with_id(self, layer_id):
        """Returns a layer given its id
        """
        self._update()
        # Expects an int so there won't be any space.
        if isinstance(layer_id, str):
            layer_id = layer_id.strip()
            layer_id = int(layer_id)
        if layer_id in self._elements:
            return self._elements[layer_id]
        print("[WARNING] id", layer_id, "doesn't exist, None is returned")
        return None

    def get(self, element_name):
        """Look for a particular layer in elements

        :param element_name: name of layer
        :return: First Layer with this idor None if nothing was found"""
        self._update()
        element_name = element_name.strip()
        for key, layer in self._elements.items():
            if layer.name == element_name:
                return layer
        print("[WARNING] layer", element_name, "doesn't exist, None is returned")
        return None

    def all(self):
        """
        :return: the list of elements' values
        """
        self._update()
        return list(self._elements.values())
