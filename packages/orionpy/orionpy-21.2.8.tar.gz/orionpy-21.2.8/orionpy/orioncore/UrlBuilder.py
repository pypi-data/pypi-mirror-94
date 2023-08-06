class _Singleton(type):
    """
    metaclass of UrlBuilder.
    type is the base metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """

        :param args: list of arguments
        :param kwargs: Dictionary [keyword arguments]= values of these arguments
        :return:
        """
        # If the class was not created yet (not in our list)...
        if cls not in cls._instances:
            # call the __call__ method of type. So, calls the class constructor
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UrlBuilder(metaclass = _Singleton):
    """Singleton class to handle url management.
    Builds the required url to use for request."""
    ORION_HEADER = "/Orion/orion"
    CHILDREN = "/__children"
    SEARCH_CHILDREN = "/__searchchildren"
    CONFIGURE = "/__configure"

    def __init__(self, main_url="https://front.arcopole.fr", portal="portal"):
        """

        :param main_url: main url to have access to the machine
        :param portal: access to the portal
        """
        self.base_url = main_url
        self.portal = portal
        

    def _api_header_url(self):
        return self.base_url + self.ORION_HEADER + "/admin/tree"

    def token_url(self):
        """
        :return: the url used to generate a token
        :Example: https://front.arcopole.fr/portal_fed_105/sharing/rest/generateToken
        """
        return self.base_url + "/" + self.portal + "/sharing/rest/generateToken"

    def self_url(self):
        """
        :return: the url used to generate a token
        :Example: https://front.arcopole.fr/portal_fed_105/sharing/rest/portals/self
        """
        return self.base_url + "/" + self.portal + "/sharing/rest/portals/self"

    def aob_config_url(self):
        """
        :return: Url with the configuration of aOB
        :Example: https://f106nfed.arcopole.fr/aob-admin/app/aobconfig.json
        """
        return self.base_url + "/aob-admin/app/aobconfig.json"

    # ----- Filter urls -----
    def filter_list_url(self):
        """
        :return: url to get access to list of defined filters
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/config/dimensions
        """
        return self._api_header_url() + "/config/dimensions"

    def filter_config_url(self):
        """
        :return: url to configure (add/remove/edit) the filters
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/config/dimensions/__configure
        """
        return self.filter_list_url() + self.CONFIGURE

    # ----- Ressource urls -----
    def resource_definition_url(self, resource_access):
        """
        :param resource_access: relative url to the resource
        :return: url for resource definition
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/SERVICES/Cannes/EspacesVerts_FeatureServer
        """
        # Layer :  + "/" + layerId
        return self.main_services_url() + "/" + resource_access

    def resource_rights_url(self, profile_id, resource_path):
        """
        :param profile_id: group for which we want service rights
        :param resource_path: the resource for which we want the rights
        :return: url to get resource rights for a group
        :Example: https://{profileRightManagementUrl}/SERVICES/Cannes/EspacesVerts_FeatureServer
        """
        return self.right_management_profiles_url(profile_id) + "/SERVICES/" + resource_path

    def resource_resolved_permissions_url(self, group_id, resource_path):
        """
        :param group_id: group for which we want resolved rights
        :param resource_path: Resource for which we want rights
        :return: url to get resolved permissions for a group on a resource
        :Example: https://{apiHeader}/rightmanagement/groups/{gId}/authorizedResources/SERVICES/{resource}
        """
        url = self._main_group_url() + \
              "/{gId}/authorizedResources/SERVICES/{path}".format(gId = group_id,
                                                                  path = resource_path)
        return url

    def resource_configuration_url(self, profile_id, resource_path):
        """
        :param profile_id: group for which want to configure resource
        :param resource_path: access to the resource
        :return: url to configure a resource for a group
        :Example: https://{api_header}/rightmanagement/profiles/{gId}/aobrights/SERVICES/{service}/__configure
        """
        return self.resource_rights_url(profile_id, resource_path) + self.CONFIGURE

    def resource_management_url(self, resource_path):
        """
        :param resource_path: access to the resource
        :return: Url to manage a resource
        :Example: https://$main_service_url$/$resourcePath$/__managing
        """
        return self.main_services_url() + "/" + resource_path + "/__managing"

    def resource_sharing_url(self, resource_id, owner='admin_aob'):
        """

        :param resource_id: id of the resource
        :param owner: resource's owner
        :return: url to get sharing informations of a service
        :Example: https://{machine}/{portal}/sharing/rest/content/users/{owner}/items/{resource_id}
        """
        url = self.base_url + \
              "/{port}/sharing/rest/content/users/{own}/items/{rId}".format(port = self.portal,
                                                                            own = owner,
                                                                            rId = resource_id)
        return url

    def resource_clear_all_url(self, resource_path):
        """
        :param resource_path: access to the resource
        :return: url to call the clearAll commands on a resource.
        :Example: https://{machine}/Orion/orion/admin/tree/object/SERVICES/Cannes/EspacesVerts_FeatureServer/__clearAll
        """
        return self.main_services_url() + "/" + resource_path + "/__clearAll"

    # ----- Cadastre resource urls -----

    def cadastre_definition_url(self):
        return self.business_definition_url("Cadastre")

    def cadastre_configuration_url(self, profile_id):
        return self.cadastre_rights_url(profile_id) + self.CONFIGURE

    def cadastre_rights_url(self, profile_id):
        """
        :param profile_id: group for which we want resource rights
        :return: url to get resource rights for a group
        :Example: https://{profileRightManagementUrl}/BUSINESS/Cadastre
        """
        return self.right_management_profiles_url(profile_id) + "/BUSINESS/Cadastre"

    # ----- Stats resource urls -----
    def businesses_children_url(self, business_access=""):
        """
        :return: url to get all services defined in orion.
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/__children
        """
        child_url = self.main_businesses_url()
        if business_access:
            child_url += "/{}".format(business_access)
        child_url += self.CHILDREN
        return child_url

    def business_definition_url(self, resource_name):
        """
        :param resource_access: relative url to the resource
        :return: url for resource definition
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre
        """
        # Layer :  + "/" + layerId
        return self.main_businesses_url() + "/" + resource_name

    def main_businesses_url(self):
        """
        :return: Main service handling url
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS
        """
        return self._api_header_url() + "/object/BUSINESS"

    def stats_resource_url(self, storage_id=""):
        resource_url = self.main_businesses_url() + "/Stats"
        if storage_id:
             resource_url += "/{}".format(storage_id)
        return resource_url

    def stats_configuration_url(self, storage_id):
        return self.stats_resource_url(storage_id) + self.CONFIGURE

    # ----- Service urls -----
    def services_children_url(self, service_access=""):
        """
        :return: url to get all services defined in orion.
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/SERVICES/__children
        """
        serv_child_url = self.main_services_url()
        if service_access:
            serv_child_url += "/{}".format(service_access)
        serv_child_url += self.CHILDREN
        return serv_child_url

    def managed_services_url(self):
        """
        :return: url to get the list of services managed by Orion
        :Example: https://front.arcopole.fr/Orion/orion/federatedLink/managedServiceList
        """
        return self.base_url + self.ORION_HEADER + "/federatedLink/managedServiceList"

    def main_services_url(self):
        """
        :return: Main service handling url
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/object/SERVICES
        """
        return self._api_header_url() + "/object/SERVICES"

    # ----- Layer urls -----
    def layer_list_url(self, service):
        """
        :param service: the service containing the layers
        :return: url to get layers of a parent service
        :Example: https://front.arcopole.fr/Orion/orion/rest/services/Nice/Proprete/MapServer/layers
        """
        return self._api_header_url() + "/rest/services/" + service + "/layers"

    # ----- Profiles urls -----
    def right_management_profiles_url(self, profile_id):
        """
        :param profile_id: id of the profile for wich we manage rights
        :return: url to manage a profile
        :Example: https://{machine}/{api}/rightmanagement/profiles/{profileId}/aobrights
        """
        return self._api_header_url() + "/rightmanagement/profiles/{pId}/aobrights".format(
            pId = profile_id)

    def profile_information_url(self, profile_id):
        """
        :param profile_id: id of the profile for wich we want informations.
        :return: url to get information on a profile.
        :Example: https://{apiHeader}/rightmanagement/profiles/{profileId}
        """
        return self._api_header_url() + "/rightmanagement/profiles/" + profile_id

    # ----- Subject urls -----
    def _main_rm_url(self):
        """
        :return: main user management url
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/users
        """
        return self._api_header_url() + "/rightmanagement"

    def subject_information_url(self, subject_type, subject_id):
        """
        :param group_id: id of the group for which we want informations.
        :return: url to get information on a specific group
        :Example: https://{machine}/{api}/rightmanagement/groups/{groupId}
        """
        return self._main_rm_url() + "/" + subject_type + "/" + subject_id

    def subject_configure_url(self, subject_type, subject_id):
        """
        :param group_id: id of the group concerned
        :return: url to configure a group
        :Example: https://{group_information_url}/__configure
        """
        return self.subject_information_url(subject_type, subject_id) + self.CONFIGURE

    def subject_list_url(self, subject_type):
        # """
        # :return: url to get the list of created group
        # :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/users/__children
        # """
        # return self._main_rm_url() + "/" + subject_type + self.CHILDREN
        """
        :param subject_type: subject type
        :return: url to get sharing informations of a service
        :Example: https://{machine}/{portal}/sharing/rest/community/{subject_type}
        """
        url = self.base_url + \
              "/{port}/sharing/rest/community/{subject_type}".format(port = self.portal,
                                                                     subject_type = subject_type)
        return url

        # (orgid:0123456789ABCDEF  -owner:esri_livingatlas -owner:esri_boundaries -owner:esri_demographics -owner:esri_nav)
# https://fmoa1071fed.arcopole.fr/portal/sharing/rest/community/groups?q=%28orgid%3A0123456789ABCDEF++-owner%3Aesri_livingatlas+-owner%3Aesri_boundaries+-owner%3Aesri_demographics+-owner%3Aesri_nav%29&sortField=&sortOrder=&num=100

        # https://fdev.ds-esrifrance.fr/Orion/orion/admin/tree/rightmanagement/users/__searchchildren?value={%22maxResults%22:200,%22first%22:0}&token=rS24EVe6vgvaASy8m41xYn3owzIxDKoI3sajtCxShCVIZBjsRyLNerLb2cIDJiF8azCXl9oKFMDcj1liAA5fNhrM6OlZQKW1v_0DVAKtLa7G9lm-MyVOEAq4LoCoRVRcQBXxx1_DH-XTqcEFL8m3JT9MX106nP_NyTEk-GMuxJ43gMMCoxGVUqwOCpVvUWbIhR_1Vk0_1hNXZEvpxVQcwjJjsdWrNDirJm8Km4WhKNM.

    # ----- User urls -----
    
    def _main_user_url(self):
        """
        :return: main user management url
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/users
        """
        return self._main_rm_url() + "/users"

    def user_list_url(self):
        """
        :return: url to get the list of created group
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/users/__children
        """
        return self._main_user_url() + self.CHILDREN

    def user_info_url(self, usr_id=None, usr_login=None, usr_domain=None):
        """Gives the url to get informations about the user

        :param usr_login: login of the user
        :param usr_domain: domain where the user is
        :return: url to get access to informations of a user
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/users/ADMIN_AMA(agol)
        """
        if usr_login and usr_domain:
            usr_id = "{}({})".format(usr_login, usr_domain)
        usr_url = self._main_user_url() + "/" + usr_id
        return usr_url

    # ----- Group urls -----
    def _main_group_url(self):
        """
        :return: main group management url
        :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/groups
        """
        return self._main_rm_url() + "/groups"

    # def group_list_url(self):
    #     """
    #     :return: url to get the list of created group
    #     :Example: https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/groups/__children
    #     """
    #     return self._main_group_url() + self.CHILDREN

    def group_information_url(self, group_id):
        """
        :param group_id: id of the group for which we want informations.
        :return: url to get information on a specific group
        :Example: https://{machine}/{api}/rightmanagement/groups/{groupId}
        """
        return self._main_group_url() + "/" + group_id

    def group_configure_url(self, group_id):
        """
        :param group_id: id of the group concerned
        :return: url to configure a group
        :Example: https://{group_information_url}/__configure
        """
        return self.group_information_url(group_id) + self.CONFIGURE

    # ----- Geonote / Project urls -----

    def base_feature_url(self, f_type):
        """
        :param f_type: type of the item (geonote or project) you will create the URL
        :return: Base Url for the item (geonote or project)
        :Example: https://front.arcopole.fr/Orion/orion/geonote or https://front.arcopole.fr/Orion/orion/project
        """
        if f_type == "Feature Collection":
            return self.base_url + self.ORION_HEADER + "/geonote"
        return self.base_url + self.ORION_HEADER + "/project"

    def search_feature_url(self, f_type):
        """
        :param f_type: type of the item (geonote or project) you will create the URL
        :return: Url to search the item (geonote or project)
        :Example: https://front.arcopole.fr/Orion/orion/geonote/search
        """
        return self.base_feature_url(f_type) + "/search"

    def search_all_feature_url(self, f_type):
        """
        :param f_type: type of the item (geonote or project) you will create the URL
        :return: Url to search the item (geonote or project)
        :Example: https://front.arcopole.fr/Orion/orion/geonote/searchAll
        """
        return self.search_feature_url(f_type) + "All"

    def data_feature_url(self, item_id, f_type):
        """
        :param item_id:
        :param f_type:
        :return: Url to get the data of the item with item_id
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/items/{item_id}/data
        """
        return self.base_feature_url(f_type) + "/content/items/" + item_id + "/data"

    def _main_feature_url(self, f_type, user):
        """
        :param f_type:
        :param user:
        :return: main url to use in methods to delete, reassign, create or delete items
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}
        """
        return self.base_feature_url(f_type) + "/content/users/" + user

    def _update_del_rea_feature(self, f_type, user, item_id):
        """
        :param f_type:
        :param user:
        :param item_id:
        :return: Url of the item with the id 'item_id' you want to update, delete or reassign
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}/items/{item_id}
        """
        return self._main_feature_url(f_type, user) + "/items/" + item_id

    def add_item_feature_url(self, f_type, user):
        """
        :param f_type:
        :param user: owner of item
        :return: Url to add the item
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}/addItem
        """
        return self._main_feature_url(f_type, user) + "/addItem"

    def update_item_feature_url(self, f_type, user, item_id):
        """
        :param f_type:
        :param user:
        :param item_id:
        :return: Url to update the item
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}/items/{item_id}/update
        """
        return self._update_del_rea_feature(f_type, user, item_id) + "/update"

    def delete_feature_url(self, f_type, user, item_id):
        """
        :param f_type:
        :param user:
        :param item_id:
        :return: Url to delete the item
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}/items/{item_id}/delete
        """
        return self._update_del_rea_feature(f_type, user, item_id) + "/delete"

    def reassign_feature_url(self, f_type, user, item_id):
        """
        :param f_type:
        :param user:
        :param item_id:
        :return: Url to reassign the item
        :Example: https://front.arcopole.fr/Orion/orion/geonote/content/users/{user}/items/{item_id}/reassign
        """
        return self._update_del_rea_feature(f_type, user, item_id) + "/reassign"

"""
    def _uri_validator(self, url):
        # TODO find out if useful to use it
        # TODO unit tests
        Check if url has a header 'http' and a body 'www.fdsqflj.com'
        :param url:
        :return: a boolean (true if valid uri. False otherwise)
        from urllib.parse import urlparse
        if url is None:
            return False
        try:
            result = urlparse(url)
            return result.scheme != "" and result.netloc != ""
        except:
            return False

"""
