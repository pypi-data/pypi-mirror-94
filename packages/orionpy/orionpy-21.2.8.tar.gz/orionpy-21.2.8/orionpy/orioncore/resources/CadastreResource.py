# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre

import json
from .Resource import RightLevel

from .BusinessResource import BusinessResource


# TODO : factorize with Resource !
class CadastreResource(BusinessResource):
    def __init__(self, resource_description):
        """

        :param resource_description: Description of the cadastre resource
        """
        super().__init__(resource_description)
        definition = resource_description["definition"]
        
        self._associated_filter = None
        self._associated_filter_id = definition['filterByCommunesId']
        self.associated_layer_id = definition['parcellesLayerReferenceIds']
        self.associated_service = definition['serviceReference']
        self.formated_service = self._get_formated_service(self.associated_service)
        self._rights = {"nominatif": RightLevel.NOMINATIF_ACCESS, "public": RightLevel.PUBLIC_ACCESS, "access": RightLevel.ACCESS}

    def _get_formated_service(self, url):
        if url == None or url == "":
            return url
        split_url = url.split('/')
        result = ""
        for i in range(0, len(split_url)-1):
            result += split_url[i]+'/'
        result = result[:-1]+'_'+split_url[len(split_url)-1]
        return result

    @property
    def associated_filter_id(self):
        """
        :return: Associated filter's id
        """
        # TODO get the full filter instead ! (How ?)
        return self._associated_filter_id

    @property
    def associated_filter(self):
        """
        :return: Associated filter (if init_filter_access was called)
        """
        if self._associated_filter is None:
            print(
                "To get associated_filter, you must call init_filter_access(associated_filter)",
                "method first, using associated_filter_id")
            return None
        return self._associated_filter

    def init_filter_access(self, associated_filter):
        """Initialize filter access

        :param associated_filter: FDU corresponding to self.associated_filter_id
        """
        # TODO : method "get_filter_access(orion)" ?
        if associated_filter.get_id() == self.associated_filter_id:
            self._associated_filter = associated_filter
        else:
            print("ERROR : you called init_filter_access not with the exact associated filter")

    # ----- Update level of right -----

    def update_right(self, group, new_right):
        """If possible, update the group's right level on this resource

        :param group: group concerned
        :param new_right: new right level (RightLevel type)
        """
        if not self._can_modify(group, new_right):
            return
        self._apply_new_right(group, new_right)

    def update_right_from_string(self, group, right_string):
        """Call the method update_right() if the right is good

        :param group: group concerned
        :param right_string: right formatted to string
        :return: True if the right is good, False if it's not good
        """
        if not self._is_right_good(right_string):
            print("[WARNING] There's an error with the right, it will not be updated")
            return False
        self.update_right(group, self._rights[right_string])
        return True

    def _is_right_good(self, right_string):
        """
        Check if the right string is good

        :param right_string:
        :return: False if the right string is not good, else return True
        """
        if right_string not in self._rights.keys():
            return False
        return True

    # ----- Activate a filter -----

    def activate_filter(self, group):
        """Activates the associated filter for a given group

        :param group: group to activate filter for
        """
        current_rights = self._get_right_structure(group)
        if self.associated_filter is None:
            print("You must call CadastreResource:init_filter_access before !")
            return
        if not self._can_activate_filter(current_rights, self.associated_filter, group):
            return
        self._activate_filter(current_rights, self.associated_filter, group)
        if not group.has_defined_filter_values(self.associated_filter):
            print('WARNING : you should define filtering values for this group and this filter')

    def _can_activate_filter(self, group_rights, filt, group=None):
        """Verify if can apply a given filter to this resource

        :param group_rights: Contains current rights on this resource
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        # TODO : also call _can_modify ?
        if not group_rights['rights']:
            print('The resource has no PUBLIC_ACCESS nor NOMINATIF_RIGHT right = can\'t activate filter.'
                  '1 FIX idea=Change right resource.update_rights(group, RightLevel.[PUBLIC_ACCESS|NOMINATIF_ACCESS])')
            return False
        if filt.get_id() in group_rights['rights'][0]['filteredDimensions']:
            print('Filter already applied, nothing to change')
            return False
        return True

    def _activate_filter(self, current_rights, filt, group):
        """Activate a filter for a group on this resource

        :param group: group for which apply filter
        """
        current_rights['rights'][0]['filteredDimensions'].append(filt.get_id())
        config_url = self._url_builder.cadastre_configuration_url(group.get_id())
        self._request_mgr.post(config_url, data = {'value': json.dumps(current_rights)})
        # print(req, req.text)
        print('Filter successfully applied on cadastre resource ',
              'for group', group.get_name())

    # ----- Deactivate a filter -----

    def deactivate_filter(self, group):
        """Deactivates the associated filter for a given group

        :param group: group to deactivate filter for
        """
        if self.associated_filter is None:
            return
        self._deactivate_filter(self.associated_filter, group)

    def _deactivate_filter(self, filt, group):
        """Remove a filter for a group on this resource

        :param filt: Filter to deactivate
        :param group: group for which disable filter"""
        current_rights = self._get_right_structure(group)
        if not self._can_deactivate_filter(current_rights, filt, group):
            return
        current_rights['rights'][0]['filteredDimensions'].remove(filt.id)
        config_url = self._url_builder.cadastre_configuration_url(group.get_id())
        self._request_mgr.post(config_url, data = {'value': json.dumps(current_rights)})
        # print(req, req.text)  # log
        print('Filter', filt.name, 'successfully deactivated on cadastre resource for',
              group.get_name())

    def _can_deactivate_filter(self, current_rights, filt, group):
        """Verify if can deactivate a given filter to this resource

        :param current_rights: Contains current rights on this resource
        :param filt: filter to deactivate
        :param group: the group for which deactivate the filter
        :return: True if all tests are passed. False otherwise
        """
        if not self._can_modify(group = group, right = ""):
            return False
        if not current_rights['rights']:
            print('The resource has no PUBLIC nor NOMINATIF right = no filter to deactivate')
            return False
        if current_rights['rights'][0]['action'] == RightLevel.NOMINATIF_ACCESS.value:
            print('The resource has a NOMINATIF right. Filter deactivation is not possible')
            return False
        # NB : as we use associated_filter, the following should never happen. (keep it ?)
        if filt.id not in current_rights['rights'][0]['filteredDimensions']:
            print('Filter to deactivate not defined for this group on this resource')
            return False
        return True

    def _can_modify(self, group, right):
        """

        :param group:
        :param right:
        :return: True if can modify and apply given right. False otherwise.
        """
        # TODO : check if right is NOMINATIF_access, public_access or access ?
        # TODO : create new method can_change_rights (cf Resource)
        if not self.is_shared_with(group):  # TODO doesn't work yet
            print('Cadastre resource must be shared with the group {gr} '
                  'to change anything'.format(gr = group.get_name()))
            return False
        if right == RightLevel.NOMINATIF_ACCESS:
            if self.associated_filter is None:
                print("You must call CadastreResource:init_filter_access before !")
                return False
            if not group.has_defined_filter_values(self.associated_filter):
                print("{gr} must have at least one filter value defined to "
                      "apply NOMINATIF_ACCESS right".format(gr = group.get_name()))
                return False
        return True

    def _apply_new_right(self, group, new_right):
        if new_right == RightLevel.NOMINATIF_ACCESS:
            self.activate_filter(group)
        current_rights = self._prepare_rights_structure(self._get_right_structure(group),
                                                        new_right)
        self._request_mgr.post(
            self._url_builder.cadastre_configuration_url(group.profile_id),
            data = {'value': json.dumps(current_rights)})
        print('Switched to', new_right.name, 'for', group.get_name(),
              'on cadastre resource !')

    def _prepare_rights_structure(self, current_rights, right_level):
        """Prepare structure that will be used for setting rights

        :param current_rights: the existing structure to modify. Allows to save applied filters
        :param right_level: new right level
        :return: the structure built.
        """
        if current_rights['rights']:  # if rights already has fields
            if right_level == RightLevel.PUBLIC_ACCESS or right_level == RightLevel.NOMINATIF_ACCESS:
                current_rights['rights'][0]['action'] = right_level.value
            elif right_level == RightLevel.ACCESS:
                current_rights['rights'] = []
        else:  # requires to build structure
            if right_level == RightLevel.PUBLIC_ACCESS:
                rights_dic = {'filteredDimensions': [],
                              'action': right_level.value}
                current_rights['rights'].append(rights_dic)
            elif right_level == RightLevel.NOMINATIF_ACCESS:
                rights_dic = {'action': right_level.value}
                current_rights['rights'].append(rights_dic)
        return current_rights

    def _get_right_structure(self, group):
        """ Gives the cadastre resource current rights for a group

        :param group: group for which we want the rights
        :return: a structure (dictionary) representing resource current rights
        """
        resource_rights_url = self._url_builder.cadastre_rights_url(profile_id = group.profile_id)

        req = self._request_mgr.get_in_python(resource_rights_url)
        # print('current :', req)
        return req

    def print_rights(self, group):
        """Prints current rights for a given group

        :param group: The group for which we want the rights
        """
        rights = self._get_right_structure(group)
        rights_str = ['Here are the rights for ', group.get_name(),
                      ' on the cadastre resource : \n']
        if rights['rights']:
            rights_str.append("\t-The right is ")
            rights_str.append(rights['rights'][0]['action'].upper() + '\n')
            if rights['rights'][0]['filteredDimensions']:
                rights_str.append("\t-Filter(s) applied :\n")
                for filt in rights['rights'][0]['filteredDimensions']:
                    rights_str.append("\t\t\t*" + filt + "\n")
        else:
            rights_str.append('\t-The right is ACCESS\n')
        print("".join(rights_str))

    def is_shared_with(self, group):  # TODO implement
        """Check if the resource is shared with a given group

        :param group: the group to check for
        :return: True if resource shared with group, false otherwise.

        .. warning:: For now, doesn't work"""
        return True

    def __str__(self):
        """Provides a string representation of a cadastre resource"""
        resource_str = 'Resource id : {}, ' \
                       'Service associé : {}, ' \
                       'Service associé formaté : {}, ' \
                       'Filtre associé : {}'.format(self.id,
                                                    self.associated_service,
                                                    self.formated_service,
                                                    self._associated_filter_id)
        return resource_str
