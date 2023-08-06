# ----Apply a filter to a Service----
#  https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/profiles/$GROUPID$/aobrights/SERVICES/Nice/Cadastre_MapServer/__configure
# POST
# param : f & token & {"isInherited":false,"rights":[{"filteredDimensions":$filterId$,
#                                                     "action":"write"}]}

# ----Save changes----
# https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/__commitPermissions
# POST
# param : f=json & token

# ----Get rights for 1 group on a service----
# https://f106fed.arcopole.fr/Orion/orion/admin/tree/rightmanagement/groups/$GROUPID$/authorizedResources/SERVICES/$SERVICE_ACCESS$
# GET
# f & token

# ----- Two ways of getting rights -----
# ---With groups
# https://f106fed.arcopole.fr/Orion/orion/admin/tree/rightmanagement/groups/$GROUP_ID$/authorizedResources/SERVICES/$LAYER_ACCESS$
# TODO what are start and maxElements attr ?
# f & start & maxElements & token
# ---With profiles
# https://f106fed.arcopole.fr/Orion/orion/admin/tree/rightmanagement/profiles/$GROUP_ID$/aobrights/SERVICES/$LAYER_ACCESS$
# f & start=0 & maxElements=-1 & token
# {
#  "isInherited":false,
#  "rights":
#   [
#      {
#       "action":"read",
#       "filteredDimensions":
#        [
#           "a513c26c-3dd9-49c7-b078-e1dc5043577d",
#           "a89eac34-a739-4fe2-99b0-f94764fac665"
#        ]
#      }
#   ]
# }

from .Layers import Layers
from .Resource import Resource
from .Tables import Tables

from .. import cfg_global


class Service(Resource):
    """Class allowing to handle service resources"""

    def __init__(self, service_id, access_url, capabilities,
                 is_hosted=False, is_managed=False, is_cadastre_resource = False):
        capa = capabilities.split(',')
        super().__init__(access_url = access_url, capabilities = capa)

        self.capabilities = capa
        self._is_managed = is_managed
        self._is_cadastre_resource = is_cadastre_resource
        self.id = service_id
        self.isHosted = is_hosted
        self._layers = Layers(self.access_url)
        self._tables = Tables(self.access_url)

    @property
    def layers(self):
        """
        :return: List of layers corresponding to this service
        """
        return self._layers

    @property
    def tables(self):
        """
        :return: List of tables corresponding to this service
        """
        return self._tables

    def is_shared_with(self, group):
        """Check if the resource is shared with a given group

        :param group: the group to check for
        :return: True if resource shared with group, false otherwise.

        .. warning:: For now, doesn't work"""
        # TODO Keep this method here ?
        # info = self._request_mgr.post_in_python(self._url_builder.resource_sharing_url(self.id))
        # groups = info['sharing']['groups']
        # if group.id in groups:
        #     return True
        # return False
        return True

    # ----- (De)activete sql filter -----

    def activate_sql_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle sql filter on a service"""
        print('Impossible to use SQL filters on a service')

    def deactivate_sql_filter(self, group, filt):
        """Overwrite this resource method as it is not possible to handle sql filter on a service"""
        print('Impossible to use SQL filters on a service')

    # ----- Deactivate right-handling from here if service associated to the cadastre resource -----

    def _can_modify(self, group, check_inheritance=True):
        if not super()._can_modify(group, check_inheritance):
            return False
        if self.is_cadastre_resource():
            print("Service associated to cadastre resource. "
                  "Use orion.services.get_cadastre_resource to handle rights for this service")
            return False
        return True

    # ----- Defines management by arcOpole Builder -----
    def enable(self):
        """Enables rights to be managed by arcOpole Builder"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        if self.is_managed():
            print('Service {} already enabled, nothing to change'.format(self.get_name()))
            return
        self._change_management(True)

    def disable(self):
        """Disables rights to be managed by arcOpole Builder"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        if not self.is_managed():
            print('Service already disabled, nothing to change')
            return
        self._change_management(False)

    def _change_management(self, enable):
        """Change a service's rights management by arcOpole Builder

        :param enable: a boolean to say if want to enable/disable the service
        """
        param = {'f': 'json'}
        if enable:
            param['value'] = '{"managed": true}'
        else:
            param['value'] = '{"managed": false}'
        management_url = self._url_builder.resource_management_url(self.access_url)
        req = self._request_mgr.get_in_python(management_url, param)
        print(req['message'])
        self._is_managed = enable

    # ----- Access methods -----

    @staticmethod
    def get_type():
        return "SERVICE"

    def get_name(self):
        """Override because the 'name' of a Service is its access url"""
        return self.access_url

    def is_cadastre_resource(self):
        """Check if the service is a cadastre_resource or not"""
        return self._is_cadastre_resource

    def __str__(self):
        """Provides a string representation of a service"""
        service_str = ['Service {}; id {};'.format(self.access_url, self.id)]
        if self._is_managed:
            service_str.append(' MANAGED')
        else:
            service_str.append(' NOT MANAGED')
        return "".join(service_str)
