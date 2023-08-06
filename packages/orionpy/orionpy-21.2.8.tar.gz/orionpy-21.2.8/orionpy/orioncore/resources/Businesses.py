# https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/profiles/authenticated/aobrights/SERVICES/SampleWorldCities_MapServer/__configure
# {"isInherited":false,"rights":[{"filteredDimensions":["32d0b429-452a-40bd-9865-5a6c6798007a"],"action":"read"}]}

from .CadastreResource import CadastreResource
from .StatsResource import StatsResource
from .StorageResource import StorageResource
from .. import cfg_global
from ..Elements import Elements


class Businesses(Elements):
    """
    Class allowing to get access to the list of business resource
    """

    def __init__(self):
        """Initialize and build our list of resources
        """
        super().__init__()

    # ----- All business resources in aOB -----
    def _update(self):
        """ Update the list of resources to make sure it's consistent with our database.
        """
        self._resources = {}
        self._build_all()

    def _build_all(self):
        """Method to build a list with all resources
        """
        node_info_url = self.url_manager.businesses_children_url()
        list_nodes = self.request.get_in_python(node_info_url)
        for node in list_nodes:
            print(node['nodeType'])
            if node['nodeType'] == 'ResourceNode':
                resource_name = node['name']
                self._add_resource_to_list(resource_name)

    def all(self):
        """
        :return: the list of elements' values
        """
        # TODO convert to list ?
        self._update()
        return self._resources

    # ----- Geting 1 resource handled by aOB -----
    def get(self, element_name):
        """Look if a particular element exist.

        :param element_name: identification of element
        :return: required element or None if nothing found
        """
        element_name = element_name.strip()
        element = self._update_one(element_name)
        if element is None:
            print("[WARNING] element", element_name, "doesn't exist, None is returned")
            return None
        return element

    def _update_one(self, element_id):
        """Update one resource required

        :param element_id: REST access url of the resource
        :return: The resource if found. None otherwise"""
        return self._create_resource(element_id)


     # ----- Getting the stats resource ----
    def get_stats_resource(self, storage_id="hosted"):
        """Get and return the stats resource if defined

        :param storage_id: id of storage define in stats resource configuration
        :return: the StatsResource or StorageResource or None if not defined.
        """
        stats_req = self._try_to_get_stats_resource(storage_id)

        if stats_req is None:
            return None
        
        if storage_id:
            return StorageResource(stats_req)
        return StatsResource(stats_req)

    def _try_to_get_stats_resource(self, storage_id=""):
        """Try to get the stats resource and handle exception if there is one."""
        stats_req = None
        try:
            stats_req = self.request.get_in_python(self.url_manager.stats_resource_url(storage_id))
        except Exception:
            stats_req = None

        return stats_req

    # ----- Getting the cadastre resource ----
    def get_cadastre_resource(self):
        """Get and return the cadastre resource if defined

        :return: the CadastreResource or None if not defined.
        """
        cadastre_req = self._try_to_get_cadastre_resource()

        if cadastre_req is None or not cadastre_req['definition']['serviceReference']:
            return None
        return CadastreResource(cadastre_req)

    def _try_to_get_cadastre_resource(self):
        """Try to get the cadastre resource and handle exception if there is one."""
        cadastre_req = None
        try:
            cadastre_req = self.request.get_in_python(self.url_manager.cadastre_definition_url())
        except Exception:
            cadastre_req = None

        return cadastre_req

    # ----- Methods for creation of a resource instance -----
    def _add_resource_to_list(self, resource_name):
        """Creates an instance of a resource and add it to the appropiated list

        :param resource_name:
        :return:
        """
        resource_instance = self._create_resource(resource_name)
        if resource_instance is None:
            return
        self._resources[resource_name] = resource_instance

    def _create_resource(self, resource_name):
        """Creates an instance of a resource if it is of a good type.

        :param resource_name:
        :return: The resource created or None if there was an error
        """
        resource_req = self._try_to_get_resource(resource_name)
        if resource_req is None or "error" in resource_req:
            print(resource_req)
            return None
        
        if resource_req['module'] == 'cadastre':
            return CadastreResource(resource_req)
        
        if resource_req['module'] == 'stats':
            return StatsResource(resource_req)

    def _try_to_get_resource(self, resource_name):
        """(FIX) Try to get a service and handle exception if there is one."""
        service_req = None
        try:
            service_req = self.request.get_in_python(self.url_manager.business_definition_url(resource_name))
        except Exception:
            service_req = None

        return service_req