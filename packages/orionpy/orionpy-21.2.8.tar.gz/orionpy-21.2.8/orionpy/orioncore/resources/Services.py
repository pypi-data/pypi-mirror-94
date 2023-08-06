# https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/profiles/authenticated/aobrights/SERVICES/SampleWorldCities_MapServer/__configure
# {"isInherited":false,"rights":[{"filteredDimensions":["32d0b429-452a-40bd-9865-5a6c6798007a"],"action":"read"}]}

from .Service import Service
from .CadastreResource import CadastreResource
from .. import cfg_global
from ..Elements import Elements


class Services(Elements):
    """
    Class allowing to get access to the list of services
    """

    def __init__(self):
        """Initialize and build our list of services
        """
        super().__init__()
        self._managed_services = {}
        self.handled_service_types = ['FeatureServer', 'MapServer', 'TileServer']

    def urls(self):
        """
        :return: services url as a list
        """
        self._update()
        return list(self._elements.keys())

    # ----- Services handled by aOB -----
    def all_managed(self):
        """Updates and returns list of managed services"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return []
        self._update_managed()
        return self._managed_services.values()

    def get_in_managed(self, element_id):
        """Look for a particular element in managed services.

        :param element_id: identification of element
        :return: required element or None if nothing found
        """
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return None
        element_id = element_id.strip()
        element = self._update_one_managed(element_id)
        if element is None:
            print("[WARNING] element", element_id,
                  "isn't managed or doesn't exist, None is returned")
            return None
        return element

    def _update_one_managed(self, service_url):
        """Update one service required

        :param service_url: REST access url of the service
        :return: The service if found. None otherwise"""
        list_managed = self.request.get_in_python(self.url_manager.managed_services_url())
        for serv_url in list_managed:
            formatted_url = Services._rreplace(serv_url, '/', '_', 1)
            if formatted_url == service_url:
                return self._create_service(service_url)
        return None

    def _update_managed(self):
        """ Update the list of managed services to make sure it's consistent with our database.
        """
        self._managed_services = {}
        # get list of services managed with orion
        list_managed = self.request.get_in_python(self.url_manager.managed_services_url())
        for serv_url in list_managed:
            formatted_url = Services._rreplace(serv_url, '/', '_', 1)
            self._add_service_to_list(formatted_url, for_managed = True)

    # ----- All services in aOB -----
    def _update(self):
        """ Update the list of services to make sure it's consistent with our database.
        """
        self._elements = {}
        self._build_all()

    def _build_all(self, service_access=""):
        """Recursive method to build a list with all services

        :param service_access: how to access to the service/folder
        """
        node_info_url = self.url_manager.services_children_url(service_access = service_access)
        list_nodes = self.request.get_in_python(node_info_url)
        for node in list_nodes:
            if 'nodeInformationData' in node:
                if service_access:
                    service_url = service_access + "/" + node['name']
                else:
                    service_url = node['name']
                if node['nodeInformationData'] == 'FOLDER':
                    self._build_all(service_url)
                elif node['nodeInformationData'] == 'SERVICE':
                    self._add_service_to_list(service_url)

    def all(self):
        """
        :return: the list of elements' values
        """
        # TODO convert to list ?
        self._update()
        return sorted(self._elements.values(),
                      key = lambda service: service.access_url.lower())

    # ----- Geting 1 service handled by aOB -----
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
        """Update one service required

        :param element_id: REST access url of the service
        :return: The service if found. None otherwise"""
        return self._create_service(element_id)

    # ----- Getting the cadastre resource ----
    def get_cadastre_resource(self):
        """Get and return the cadastre resource if defined

        :return: the CadastreResource or None if not defined.

        .. deprecated:: AOB 1.4
            Use :func:`orion.businesses.get_cadastre_resource` instead.
        """
        cadastre_req = self._try_to_get_cadastre_resource()

        if cadastre_req is None or not cadastre_req['definition']['serviceReference']:
            return None
        return CadastreResource(cadastre_req)

    def _try_to_get_cadastre_resource(self):
        """Try to get the cadastre resource and handle exception if there is one."""
        cadastre_req = None
        try:
            cadastre_req = self.request.get_in_python(
                self.url_manager.cadastre_definition_url())
        except Exception:
            cadastre_req = None

        return cadastre_req

    # ----- Methods for creation of a service instance -----
    def _add_service_to_list(self, service_url, for_managed=False):
        """Creates an instance of a service and add it to the appropiated list

        :param service_url:
        :param for_managed: parameter saying if fills up common list or list of managed services
        :return:
        """
        service_instance = self._create_service(service_url)
        if service_instance is None:
            return
        if for_managed:
            self._managed_services[service_url] = service_instance
        else:
            self._elements[service_url] = service_instance

    def _create_service(self, service_url):
        """Creates an instance of a service if it is of a good type.

        :param service_url:
        :return: The service created or None if there was an error
        """
        if not self._good_service_type(service_url):
            return None
        # Handle if service ""of good type"" but doesn't exist.
        service_req = self._try_to_get_service(service_url)
        if service_req is None or "error" in service_req:
            # print(service['error'])
            return None
        service = service_req['definition']
        if 'isManaged' in service:  # TODO test on env.is_federated
            is_managed = service['isManaged']
        else:
            is_managed = False
        # Doing so improves retro compatibility for OrionPy
        if 'isCadastreResource' in service:
            is_cadastre_resource = service['isCadastreResource']
        else:
            is_cadastre_resource = False
        return Service(service['portalItemId'], service_url, service['capabilities'],
                       is_managed = is_managed, is_cadastre_resource = is_cadastre_resource)

    def _try_to_get_service(self, service_url):
        """(FIX) Try to get a service and handle exception if there is one."""
        service_req = None
        try:
            service_req = self.request.get_in_python(
                self.url_manager.resource_definition_url(service_url))
        except Exception:
            service_req = None

        return service_req

    def _good_service_type(self, service_name):
        """Look if a given service is of a type that can be managed by aob_admin

        :param service_name: service name. Ends with the service type
        :return: True if the service is of a type handled. False otherwise
        """
        for handled_type in self.handled_service_types:
            if (service_name.lower()).endswith(handled_type.lower()):
                return True
        return False

    @staticmethod
    def _rreplace(original_str, old, new, count):
        """In original_str, replace count occurences of character old by new.
        Starting from the end of the string

        :param original_str:
        :param count:
        :return:
        """
        li = original_str.rsplit(old, count)
        return new.join(li)
