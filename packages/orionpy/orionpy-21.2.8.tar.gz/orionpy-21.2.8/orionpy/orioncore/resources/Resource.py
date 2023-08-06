# *** Obtenir les droits résolus ***
# https://{orionHeadAdmin}/rightmanagement/groups/{group_id}/authorizedResources/SERVICES/{resourcePath}

# *** Obtenir les droits configurés ***
# https://{orionHeadAdmin}/rightmanagement/profiles/{profileId}/aobrights/SERVICES/{resourcePath}


import abc
import json
from enum import Enum, unique

from .. import cfg_global
from ..RequestManager import RequestManager
from ..Filter import _FDUFilter, _SQLFilter
from ..UrlBuilder import UrlBuilder


@unique  # Ensures that enum's values are unique
class RightLevel(Enum):
    """An enumeration.
    Represents the different levels of rights which are possible to apply
    The values being the ones used in the request."""
    # TODO handle RightLevel.NO_ACCESS
    NO_ACCESS = "nothing"
    ACCESS = "access"
    READ = "read"
    WRITE = "write"
    PUBLIC_ACCESS = "public_access"
    NOMINATIF_ACCESS = "nominatif_access"


class Resource(metaclass = abc.ABCMeta):
    """
    Common abstract class for resources (service, layer, ...)
    """

    # TODO factorize prints and .format()

    def __init__(self, access_url, capabilities="", parent_access="", is_managed=False):
        self.access_url = access_url
        self.capa = capabilities
        self.parent_access = parent_access
        self._url_builder = UrlBuilder()
        self._request_mgr = RequestManager()
        self._is_managed = is_managed
        self.name = "TMP"
        self.type = ""
        self.groups = []

    # ----- Activate a filter -----

    def activate_fdu_filter(self, group, filt):
        # TODO method force_fdu_filter(group, filter) ?
        """Add a FDU filter for a group on this resource

        :param filt: The filter (FDU) to apply
        :param group: group for which apply filter
        """
        current_rights = self._get_right_structure(group)
        if not self._can_activate_FDU(current_rights, filt, group):
            return
        self._activate_filter(current_rights, filt, group)
        if not group.has_defined_filter_values(filt):
            print('WARNING : you should define filtering values for this group and this filter')

    def activate_sql_filter(self, group, filt):
        # TODO method force_sql_filter(group, filter) ?
        """Add a SQL filter for a group on this resource

        :param filt: The filter (FDU) to apply
        :param group: group for which apply filter
        """
        current_rights = self._get_right_structure(group)
        if not self._can_activate_SQL(current_rights, filt, group):
            return
        self._activate_filter(current_rights, filt, group)

    def _activate_filter(self, current_rights, filt, group):
        """Activate a filter for a group on this resource

        :param filt: The filter to apply
        :param group: group for which apply filter
        """
        current_rights['rights'][0]['filteredDimensions'].append(filt.id)
        config_url = self._url_builder.resource_configuration_url(group.get_id(), self.access_url)
        self._request_mgr.post(config_url, data = {'value': json.dumps(current_rights)})
        # print(req, req.text)
        print('Filter', filt.name, 'successfully applied on resource', self.access_url,
              'for group', group.get_name())

    # ----- Deactivate a filter -----

    def deactivate_fdu_filter(self, group, filt):
        """Remove a (FDU) filter for a group on this resource

        :param filt: Filter to deactivate
        :param group: group for which disable filter"""
        self._deactivate_filter(filt, group)

    def deactivate_sql_filter(self, group, filt):
        """Remove a (SQL) filter for a group on this resource

        :param filt: Filter to deactivate
        :param group: group for which disable filter"""
        self._deactivate_filter(filt, group)

    def _deactivate_filter(self, filt, group):
        """Remove a filter for a group on this resource

        :param filt: Filter to deactivate
        :param group: group for which disable filter"""
        current_rights = self._get_right_structure(group)
        if not self._can_deactivate_filter(current_rights, filt, group):
            return
        current_rights['rights'][0]['filteredDimensions'].remove(filt.id)
        config_url = self._url_builder.resource_configuration_url(group.get_id(), self.access_url)
        self._request_mgr.post(config_url, data = {'value': json.dumps(current_rights)})
        # print(req, req.text)  # log
        print('Filter', filt.name, 'successfully deactivated on resource', self.access_url,
              'for', group.get_name())

    # ----- Access to current/parent rights -----

    def _get_right_structure(self, group):
        """ Gives the resource current rights for a group

        :param group: group for which we want the rights
        :return: a structure (dictionary) representing resource current rights
        """
        resource_rights_url = self._url_builder.resource_rights_url(profile_id = group.profile_id,
                                                                    resource_path = self.access_url)

        req = self._request_mgr.get_in_python(resource_rights_url)
        # print('current :', req)
        return req

    def get_resolved_right(self, group):
        """Returns the resolved right

        :param group: group for which we want the rights
        :return: The right level's value
        """
        resolved_url = self._url_builder.resource_resolved_permissions_url(group.get_id(),
                                                                           self.access_url)
        resolved_rights = self._request_mgr.get_in_python(resolved_url)
        resolved_perm_key = 'resolvedPermissions'
        if RightLevel.WRITE.value in resolved_rights[resolved_perm_key] \
                and resolved_rights[resolved_perm_key][RightLevel.WRITE.value]['permission']:
            return RightLevel.WRITE
        if RightLevel.READ.value in resolved_rights[resolved_perm_key] \
                and resolved_rights[resolved_perm_key][RightLevel.READ.value]['permission']:
            return RightLevel.READ
        return RightLevel.ACCESS

    def print_rights(self, group):
        """Prints current rights for a group

        :param group: The group for which we want the rights
        """
        rights = self._get_right_structure(group)
        rights_str = ['Here are the rights for ', group.get_name(), ' on ',
                      self.access_url, ' : \n']
        if rights['isInherited']:
            rights_str.append("\t-Right inherited\n")
            rights_str.append("\t-The right is ")
            rights_str.append(self.get_resolved_right(group).value.upper() + '\n')
        else:
            rights_str.append("\t-Right not inherited\n")
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

    def _get_parent_rights(self, group):
        """ Get a resource parent's current rights for a group

        :param group: id of the group for wich we want information
        :return: the resource parent's rights for this group
        """
        req = self._request_mgr.get_in_python(
            self._url_builder.resource_rights_url(group.get_id(), self.parent_access))
        print('parent :', req)
        return req

    # ----- Update level of right -----

    def clear_all_rights(self):
        """
        If possible, clears given rights and filters on a resource.
        However, it will not remove sharing accesses.
        """
        if not self.is_managed():
            return
        self._request_mgr.post(
            self._url_builder.resource_clear_all_url(self.access_url)
        )
        print('Cleared all rights on resource ', self.access_url)

    def force_right(self, group, new_right):
        """Method forcing a right on a resource

        :param group: group concerned
        :param new_right: new right level (RightLevel type)
        """
        # Enables right handling if not already done.
        if cfg_global.is_federated and not self.is_managed() and self.get_type() == "SERVICE":
            self.enable()

        if not self._can_modify(group, check_inheritance = False) or \
                not self._can_change_rights(group, new_right):
            # print('Impossible to change right but will at least try to disable inheritance')
            self.disable_inheritance(group)
            return

        # Applies the new configuration
        self._apply_new_right(group, new_right, disable_inheritance = True)

    def update_right(self, group, new_right):
        """If possible, update the group's right level on this resource

        :param group: group concerned
        :param new_right: new right level (RightLevel type)
        """
        # Check if can modify anything about the rights
        if not self._can_modify(group) or \
                not self._can_change_rights(group, new_right):
            return
        # Applies the new configuration
        self._apply_new_right(group, new_right)

    def _apply_new_right(self, group, new_right, disable_inheritance=False):
        """Prepares right structure and apply right modification on the resource

        :param group: group concerned
        :param new_right: new right level (RightLevel type)
        :param disable_inheritance: If it is required to disable inheritance or not
        :return:
        """
        current_rights = self._prepare_rights_structure(self._get_right_structure(group),
                                                        new_right,
                                                        disable_inheritance)
        self._request_mgr.post(
            self._url_builder.resource_configuration_url(group.profile_id, self.access_url),
            data = {'value': json.dumps(current_rights)})
        # print(answer, answer.text)  # log
        print('Switched to', new_right.name, 'for', group.get_name(),
              'on resource', self.access_url)

    def _prepare_rights_structure(self, current_rights, right_level, disable_inheritance=False):
        """Prepare structure that will be used for setting rights

        :param current_rights: the existing structure to modify. Allows to save applied filters
        :param right_level: new right level
        :return: the structure built.
        """
        if current_rights['rights']:  # if rights already has fields
            if right_level == RightLevel.READ or right_level == RightLevel.WRITE:
                current_rights['rights'][0]['action'] = right_level.value
            elif right_level == RightLevel.ACCESS:
                current_rights['rights'] = []
        else:  # requires to build structure
            if right_level == RightLevel.READ or right_level == RightLevel.WRITE:
                rights_dic = {'filteredDimensions': [],
                              'action': right_level.value}
                current_rights['rights'].append(rights_dic)
        if disable_inheritance:
            current_rights['isInherited'] = False
        return current_rights

    # ----- Tests validity of modification -----

    def is_shared_with(self, group):  # TODO implement this for every resource type
        """Check if the resource is shared with a given group

        :param group: the group to check for
        :return: True if resource shared with group, false otherwise.

        .. warning:: For now, only work for services"""
        # si id groupe dans groups, true else false
        return True

    def _has_parent(self):
        """Check if the resource has a parent

        :return: if no parent (a service), returns an empty string(=False).
        Otherwise, returns parent access (non-emptystring/True)
        """
        return self.parent_access

    def is_managed(self):
        """Check if resource's rights are managed by aOB

        :return: True if resource managed by aOB, False otherwise."""
        if not cfg_global.is_federated:
            return True  # avoid problems during right configuration
        return self._is_managed

    def has_inherited_right(self, group):
        """Checks if right is inherited for group

        :param group: group for which look for
        :return:
        """
        current_rights = self._get_right_structure(group)
        return current_rights['isInherited']

    def _can_modify(self, group, check_inheritance=True):
        """Verify if can change anything about rights on this resource

        :param group: Group for which modify anything about rights
        """
        if not self.is_managed():
            print('You must enable {rs} to handle rights first : '
                  'Use Service::enable()'.format(rs = self.get_name()))
            return False
        if not self.is_shared_with(group):  # TODO doesn't work yet
            print('{rs} must be shared with the group {gr} '
                  'to change anything'.format(rs = self.get_name(), gr = group.get_name()))
            return False
        if check_inheritance and self.has_inherited_right(group):
            print("You must disable inheritance on {rs} for group {gr} to change anything : "
                  "Use the disable_inheritance(group) method".format(rs = self.get_name(),
                                                                     gr = group.get_name()))
            return False
        return True

    def _can_change_rights(self, group, right_to_apply):
        """Verify if can change the right level for this resource

        :param group: id of the group concerned by this modification
        :param right_to_apply: New right level to apply
        """
        if right_to_apply == RightLevel.WRITE \
                and self.capa and 'Editing' not in self.capa:
            print('Impossible to add editing write '
                  'for group {gr} on {rs}'.format(gr = group.get_name(),
                                                  rs = self.get_name()))
            return False

        current_right = self.get_resolved_right(group)
        if current_right == right_to_apply:
            # print('Right already defined as', right_to_apply.value.upper(),
            #       'for group {gr} on {rs}, nothing to change'.format(rs = self.get_name(),
            #                                                          gr = group.get_name()))
            return False
        return True

    # ----- Tests validity to (de)activate filter -----

    def _can_activate_SQL(self, group_rights, filt, group):
        """Verify if can apply a SQL filter to this resource

        :param group_rights: Contains current rights on this resource
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not isinstance(filt, _SQLFilter):
            print('Filter must be of SQL type')
            return False
        if not self._can_activate_filter(group_rights, filt, group):
            return False
        return True

    def _can_activate_FDU(self, group_rights, filt, group):
        """Verify if can apply a FDU filter to this resource

        :param group_rights: Contains current rights on this resource
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not isinstance(filt, _FDUFilter):
            print('Filter must be of FDU type')
            return False
        if not self._can_activate_filter(group_rights, filt, group):
            return False
        return True

    def _can_activate_filter(self, group_rights, filt, group):
        """Verify if can apply a given filter to this resource

        :param group_rights: Contains current rights on this resource
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not self._can_modify(group = group):
            return False
        if not group_rights['rights']:
            print('The resource has no READ nor WRITE right = no filter to activate.'
                  '1 FIX idea= Change right resource.update_rights(group, RightLevel.[READ|WRITE])')
            return False
        if filt.id in group_rights['rights'][0]['filteredDimensions']:
            print('Filter already applied, nothing to change')
            return False
        return True

    def _can_deactivate_filter(self, current_rights, filt, group):
        """Verify if can deactivate a given filter to this resource

        :param current_rights: Contains current rights on this resource
        :param filt: filter to apply
        :param group: the group for which apply the filter
        :return: True if all tests are passed. False otherwise
        """
        if not self._can_modify(group = group):
            return False
        if not current_rights['rights']:
            print('The resource has no READ nor WRITE right = no filter to activate')
            return False
        if filt.id not in current_rights['rights'][0]['filteredDimensions']:
            print('Filter to deactivate not defined for this group on this resource')
            return False
        return True

    # ----- Change inheritance -----

    def enable_inheritance(self, group):
        """Enables inheritance

        :param group: the group for which change inheritance
        """
        self._change_inheritance(group, True)

    def disable_inheritance(self, group):
        """Disable inheritance

        :param group: the group for which change inheritance
        """
        self._change_inheritance(group, False)

    def _change_inheritance(self, group, new_inheritance):
        """Disable or enable inheritance of rights for the group on this resource

        :param group: the group for which change inheritance
        :param new_inheritance: a boolean. True if inherit, false otherwise
        """
        if not self._can_modify(group, check_inheritance = False):
            return False
        group_rights = self._get_right_structure(group)
        if group_rights['isInherited'] == new_inheritance:
            # print('Nothing to change in inheritance')
            return False

        group_rights['isInherited'] = new_inheritance

        if not group_rights['isInherited']:  # if disable inheritance, need to prepare structure...
            right = self.get_resolved_right(group)
            self._prepare_rights(group_rights, right)

        # Does the action of changing inheritance
        self._request_mgr.post(
            self._url_builder.resource_configuration_url(group.profile_id, self.access_url),
            data = {'value': json.dumps(group_rights)})

        inherit_str = 'enabled' if new_inheritance else 'disabled'
        print('Inheritance {inh} for {gr} on {rs}'.format(inh = inherit_str,
                                                          gr = group.get_name(),
                                                          rs = self.get_name()))

    # ----- Access methods -----
    def get_access_url(self):
        return self.access_url

    def get_name(self):
        return self.name

    @staticmethod
    def get_type():
        # TODO find another way to do this
        pass

    @staticmethod
    def _prepare_rights(group_rights, action):
        """Prepares the right structure when disable_inheritance

        :param group_rights: structure to modify
        :param action: action to apply (RightLevel type)
        """
        if action == RightLevel.ACCESS:
            group_rights['rights'] = []
        elif group_rights['rights']:
            # This allows to save filters if set
            group_rights['rights'][0]['action'] = action.value
        else:  # an empty list and needs to create structure.
            group_rights['rights'] = [{'action': action.value}]
