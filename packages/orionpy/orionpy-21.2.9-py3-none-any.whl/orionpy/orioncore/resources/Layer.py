from .Fields import Fields
from .Resource import Resource


class Layer(Resource):
    # TODO add class LayerGroup inheriting from Layer ?
    """Class allowing to handle layers resources (components of a service)
    """

    def __init__(self, description, parent_service_url, capabilities, is_managed=False):
        """Layer constructor

        :param parent_service_url: The containing service formatted url
        :param capabilities: right capabilities on this layer
        :param is_managed: Say if rights are managed by aOB
        :param description: a dictionary containing a layer definition
        parentLayerId = -1 if no parentLayer
        subLayerIds : null if no sublayers (not a group)
        defaultVisibility (bool) : ??
        """
        capa = capabilities.split(',')
        super().__init__(parent_service_url + "/" + str(description['id']), capabilities = capa,
                         parent_access = parent_service_url, is_managed = is_managed)
        self.id = str(description['id'])
        self.name = description['name']

        # parentLayerId is used if the layer has a group-layer parent
        self.parentLayerId = description['parentLayerId']

        # This parameter is used if the layer is actually a group of layer.
        self.subLayerIds = description['subLayerIds']
        self._is_group = True if self.subLayerIds else False

        self.defaultVisibility = description['defaultVisibility']
        self.minScale = description['minScale']
        self.maxScale = description['maxScale']
        self.capabilities = capa

        self._fields = Fields(self.parent_access, self.id)

    @property
    def fields(self):
        """
        :return: List of fields corresponding to this layer
        """
        return self._fields

    # ----- Test methods -----

    def _can_activate_FDU(self, group_rights, filt, group):
        """Verify if can apply a given filter to this layer

        :param group_rights: Contains current rights on this layer
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not super()._can_activate_FDU(group_rights, filt, group):
            return False
        for attr in filt.get_fields():
            if self.fields.get(attr) is None:
                print('In order to apply filter on a layer, its attributes has to be in fields')
                return False
        return True

    def is_group(self):
        """Method saying if the layer is a group of layers or not"""
        return self._is_group

    def has_parent_layer(self):
        """Allows to know if a layer is in a group or not."""
        return self.parentLayerId != -1

    def has_sub_layers(self):
        """Allows to know if a layer has sub layers"""
        return self.subLayerIds is not None

    # ----- Access methods -----

    def get_sub_layers_ids(self):
        """If this is a group of layers, returns list of its sublayers"""
        if self.has_sub_layers():
            return self.subLayerIds
        print('[WARNING] Layer {}({}) not a group of layers. or has no sub-layers.'
              'None is returned'.format(self.name,
                                        self.id))
        return None

    def get_parent_layer_id(self):
        """Returns the parent layer's id (if there is one)"""
        if self.parentLayerId == -1:
            print('[WARNING] no parent layer. None is returned')
            return None
        return self.parentLayerId

    @staticmethod
    def get_type():  # TODO mention LAYER-GROUP here ?
        return "LAYER"

    def __str__(self):
        layer_type = 'group of layers' if self.is_group() else 'simple layer'
        layer_str = [
            'Layer {}; name {}; type {}; for Service {}.'.format(self.id, self.name, layer_type,
                                                                self.parent_access)]
        if self.is_group() and self.has_sub_layers():
            layer_str.append("\n\tIts sub-layers'IDs are : {}".format(self.get_sub_layers_ids()))

        return "".join(layer_str)
