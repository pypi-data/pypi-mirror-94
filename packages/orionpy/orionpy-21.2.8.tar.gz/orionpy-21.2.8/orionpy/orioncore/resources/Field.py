from .Resource import Resource, RightLevel


# https://{machine}/{api}/object/SERVICES/{service}/{layerId}/{fieldId}


class Field(Resource):
    """Class allowing to get access and manage a field"""

    # TODO get all corresponding values
    def __init__(self, description, service_url, layer_id, capa, is_managed=False):
        capa = capa.split(',')
        super().__init__(service_url + "/" + str(layer_id) + "/" + str(description['name']),
                         capabilities = capa, parent_access = service_url + "/" + str(layer_id),
                         is_managed = is_managed)
        self.name = description['name']
        self.field_type = description["type"]
        self.alias = description["alias"]
        self.parentUrl = service_url
        self.layerId = layer_id
        self.type = "FIELD"

    # ----- (De)activete filter -----

    def activate_fdu_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle filter for a field"""
        print('Impossible to modify filters on a field')

    def deactivate_fdu_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle filter for a field"""
        print('Impossible to modify filters on a field')

    def activate_sql_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle filter for a field"""
        print('Impossible to modify filters on a field')

    def deactivate_sql_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle filter for a field"""
        print('Impossible to modify filters on a field')

    def _can_change_rights(self, group, right_to_apply):
        """Verify if can change the right level for this resource

        :param right_to_apply: New right level to apply
        :param group: id of the group concerned by this modification
        """
        if not super()._can_change_rights(group, right_to_apply):
            return False
        if right_to_apply == RightLevel.WRITE:
            # This case exist only when want to apply editing right
            parent_rights = self._get_parent_rights(group)
            if parent_rights['rights'][0]['action'] != 'write':
                print('To give edit right on a field, containing layer needs to have it as well')
                return False
        return True

    @staticmethod
    def get_type():
        return "FIELD"

    def get_name(self):
        return self.alias

    def __str__(self):
        return "Field {}; alias {}; layer {}; service {}".format(self.name, self.alias,
                                                                 self.layerId, self.parentUrl)
