# ---- Get informations about a subject----
# https://{machine}/{api}/rightmanagement/groups/{subject}
# GET
# f & token

# ---- Get rights on resources ----
# https://{machine}/{api}/rightmanagement/groups/{subject}/authorizedResources

# ---- Get rights on services ----
# {getRightsResources_URL}/SERVICES

# ---- Get right on a particular service ----
# {getRightServices_URL}/{service}

# ---- Get rights on a layer ----
# {getRightsParticularService_URL}/{layer}

# ---- Get rights on a field ----
# {getRightsLayer_URL}/{field}

# ---- Set filtering values ----
# {groupInformationURL}/__configure
# value = {"name":$GROUP_ID$,
#          "domaine":$GROUP_DOMAIN$,
#          "perimeters":
#               [{"dimension":$FILTER_ID$,
#                 "valeures":$ONE_SELECTED_FILTERING_VAL$
#                 }*
#                ]
#         }
# https://{machine}/{api}/rightmanagement/groups/{subject}
#    {
#     "title":"Organisation",
#     "name":"org",
#     "domain":"default",
#     "isSuperAdmin":false,
#     "perimeters": # defined filtering values
#      [
#      ],
#     "properties":
#      {
#       "builtinRole":"authenticated"
#      }
#    }

# "name": "128703724fce49358406f2dfcf8d43aa",
# "nodeType": "GroupNode",
# "title": "Accueil"

import json

from .Exceptions import FilteringValuesError
from .Filter import _FDUFilter
from .RequestManager import RequestManager
from .UrlBuilder import UrlBuilder


class Subject:
    # TODO way too much method to update filtering values
    """Single subject-data handling class"""

    def __init__(self, title, id, subject_type, profile_id = None):
        self.title = title
        # NB : for 'org' and 'public' groups, id is the builtinrole.
        self.id = id
        self.subject_type = subject_type
        if profile_id is not None:
            self._profile_id = profile_id
        self._url_builder = UrlBuilder()
        self._request_mgr = RequestManager()
        self.perimeters_key = 'perimeters'
        self.filter_val_key = 'valeures'
        self.filter_id_key = 'dimension'

    # ----- Updating filtering values -----

    @property
    def profile_id(self):
        if self.is_system_subject():
            return self._profile_id
        return self.id

    def set_several_filter_values(self, filters_and_values):
        """Update/Add filtering values for several FDU filters on this subject
        For other filters, keep the values already defined.

        :param filters_and_values: A dictionary : [filter] = corresponding filtering values.
        """
        for filt, filtering_values in filters_and_values.items():
            # TODO : improve it to send only one request.
            self.set_filter_values(filt, filtering_values)

    # TODO : deprecates it. Create new method 'empty_filtering_values()'
    def reset_all_filters_values(self, filters_and_values):
        """Re-set filtering values for several FDU filters (with only one request)
        If there is existing filtering values for this subject, removes it.

        :param filters_and_values: A dictionary : [filter] = corresponding filtering values.
        """
        subject_information = self._request_mgr.get_in_python(
            self._url_builder.subject_information_url(self.subject_type, self.id))
        # as we will redefine filter values, erase previous ones
        subject_information[self.perimeters_key] = []
        for filt, filtering_values in filters_and_values.items():
            if not isinstance(filt, _FDUFilter):
                print('[ERROR] Only possible to defined filtering values on a FDU filter')
                continue
            if filtering_values:
                subject_information[self.perimeters_key].append(
                    self._build_perimeters(filt, filtering_values))
            else:
                print('[ERROR] : selected_filtering_values must not be empty')

        self._apply_configuration(subject_information)

    # TODO : allow 'labels' to be values as well ?
    def set_filter_values(self, fdu_filter, labels=None,
                          add_all_values=False):
        """Update filtering values for one FDU filter on this subject

        :param fdu_filter: The FDU filter for which set filtering values
        :param labels: list of filtering values selected
        :param add_all_values: boolean to specify if want to add each value
        :raises FilteringValuesError: if problem in parameters
        """
        try:
            if not isinstance(fdu_filter, _FDUFilter):
                raise FilteringValuesError('[ERROR] Can only define filtering values on a FDU')
            # Check that the good arguments are given
            if not add_all_values:
                if labels is None:
                    raise FilteringValuesError('[ERROR] If add_all False, labels must be provided.')
                elif not labels:
                    raise FilteringValuesError('[ERROR] "labels" can\'t be an empty list')
        except FilteringValuesError as e:
            print(e.args)
            return

        if add_all_values:
            labels = fdu_filter.get_labels()

        # Get current filtering values defined for this subject
        subject_information = self._subject_information_minus_filter(fdu_filter)
        # add values for our filter
        subject_information[self.perimeters_key].append(
            self._build_perimeters(fdu_filter, labels))
        # Applies change and print result ({type:configue} if ok)
        self._apply_configuration(subject_information)

    def add_filtering_values(self, fdu_filter, labels):
        """Adds filtering values to a subject if not already set

        :param fdu_filter: the filter for which set filtering values
        :param labels: a list containing labels to add in filtering values
        """
        subject_info = self.get_subject_informations()
        f_index = self._get_filter_index(fdu_filter.get_id(),
                                         subject_info[self.perimeters_key])
        if f_index is None:  # Nothing was found, need to create strcture for filter
            self.set_filter_values(fdu_filter, labels)
            return

        # Get filtering values already defined on this filter.
        filter_values = subject_info[self.perimeters_key][f_index][self.filter_val_key].split(',')

        something_to_add = False
        for label in labels:  # For the labels we want to add...
            # If the label isn't already defined, does it
            if label not in filter_values:
                something_to_add = True
                filter_values.append(label)

        if something_to_add:
            # Applies the new configuration
            self._apply_filtering_values(subject_info, f_index, filter_values)

    def remove_filtering_values(self, fdu_filter, labels):
        """Removed filtering values to a subject if already set

        :param fdu_filter: the filter for which remove filtering values
        :param labels: a list containing labels to remove in filtering values
        """
        subject_info = self.get_subject_informations()
        f_index = self._get_filter_index(fdu_filter.get_id(),
                                         subject_info[self.perimeters_key])
        if f_index is None:  # Nothing was found, nothing to change !
            return

        # Get filtering values already defined on this filter.
        filter_values = subject_info[self.perimeters_key][f_index][self.filter_val_key].split(',')
        if not filter_values:  # If no filtering value, nothing to remove !
            return

        something_to_remove = False
        for label in labels:  # For the labels we want to delete...
            # If label is defined, remove it
            if label in filter_values:
                something_to_remove = True
                filter_values.remove(label)

        if something_to_remove:
            # Applies the new configuration
            self._apply_filtering_values(subject_info, f_index, filter_values)

    def set_filter_field_values(self, fdu_filter, values, field):
        """Update filtering values for one FDU filter on this subject.
        Instead of label, use a field values

        :param fdu_filter: The FDU filter for which set filtering values
        :param values: list of filtering values selected
        :param field: field with values
        :raises FilteringValuesError: if problem in parameters
        """
        try:
            if not isinstance(fdu_filter, _FDUFilter):
                raise FilteringValuesError('[ERROR] Can only define filtering values on a FDU')
            if values is None or not values:
                raise FilteringValuesError('[ERROR] "values" can\'t be an empty list')
            if not field:
                raise FilteringValuesError('[ERROR] "field" must be provided')
        except FilteringValuesError as e:
            print(e.args)
            return

        # Get current filtering values defined for this subject
        subject_information = self._subject_information_minus_filter(fdu_filter)
        # add values for our filter
        subject_information[self.perimeters_key].append(
            self._build_perimeters(fdu_filter, values, field))

        # Applies change and print result ({type:configue} if ok)
        self._apply_configuration(subject_information)

    def _apply_filtering_values(self, subject_info, filter_index, filter_values):
        """Applies modification of filtering values for a filter on a subject."""
        subject_info[self.perimeters_key][filter_index][self.filter_val_key] = ','.join(
            filter_values)
        self._apply_configuration(subject_info)

    def _get_filter_index(self, filter_id, filtering_values):
        """Search if a filter has defined values in a subject. If so, returns its index

        :param filter_id: filter to look for
        :param filtering_values: list of defined filtering values for this subject
        :return: filter index if found. None otherwise
        """
        return next((index for (index, filt) in enumerate(filtering_values)
                     if filt[self.filter_id_key] == filter_id), None)

    def _get_filter_values(self, filter_id):
        """Returns filtering values defined for this subject on a given filter"""
        info_url = self._url_builder.subject_information_url(self.subject_type, self.id)
        subject_info = self._request_mgr.get_in_python(info_url)
        for perim in subject_info[self.perimeters_key]:
            if perim[self.filter_id_key] == filter_id:
                return perim[self.filter_val_key]
        return None

    def _apply_configuration(self, config):
        """Applies a pre-defined configuration to our subject

        :param config: the configuration required.
        """
        self._request_mgr.get(self._url_builder.subject_configure_url(self.subject_type, self.id),
                              params = {'value': json.dumps(config)})
        print('Successfully applied change on configuration for subject "{}" !'.format(self.title))

    def _subject_information_minus_filter(self, filter_to_set):
        """Get the current subject configuration, removing the selected filter values

        :param filter_to_set: filter for which remove filtering values if it's defined
        :return: A dictionary representing the formatted subject configuration
        """
        subject_information = self.get_subject_informations()
        self._remove_current_filter_value(subject_information[self.perimeters_key], filter_to_set.id)
        return subject_information

    def _build_perimeters(self, filter_concerned, filtering_values, field=""):
        """Builds the associtation filter-filtering values. Formatted as required by the API.

        :param filter_concerned: the filter for which associate filtering values
        :param filtering_values: the filtering values to add to this filter
        :param field: (optional) corresponding field if filtering_values are field value
        :return: association filter-values as : {'dimension': filter_id, 'valeures':"val1, val2..."
        """
        approved_values = []
        # Handle if there are values in selected_filtering_values which aren't set for filter
        for filtering_value in filtering_values:
            if filter_concerned.is_label_defined(filtering_value):
                approved_values.append(filtering_value)
            elif field and filter_concerned.is_field_value_defined(field, filtering_value):
                approved_values += filter_concerned.get_labels_for(field, filtering_value)
            else:
                print('Value', filtering_value, 'not defined for this filter. It will not be set')
        return {self.filter_id_key: filter_concerned.id,
                self.filter_val_key: ','.join(approved_values)}

    def _remove_current_filter_value(self, perimeters, filter_id):
        """If filtering values were already defined for a selected filter, removes it

        :param perimeters: the list of filter values to look in
        :param filter_id: the filter to look for (and remove if found)
        """
        # TODO find a better name
        # TODO use index(filter_id) and pop(index) methods.
        for filtering_values in perimeters:
            if filtering_values[self.filter_id_key] == filter_id:
                perimeters.remove(filtering_values)
                return
        print('Defining filtering values for', filter_id)

    # ----- Test methods -----

    def has_defined_filter_values(self, fdu_filter):
        """Check if the subject has filtering values defined for a specified filter

        :param fdu_filter: filter to check for
        :return: True if subject has defined filtering values, False otherwise
        """
        info_url = self._url_builder.subject_information_url(self.subject_type, self.id)
        subject_info = self._request_mgr.get_in_python(info_url)
        for perim in subject_info[self.perimeters_key]:
            if perim[self.filter_id_key] == fdu_filter.id:
                return True
        return False

    def has_label_set_for_filter(self, fdu_filter, label):
        """Check if a specific label is enabled as filtering values for this subject

        :return: True if this label is activated. False otherwise."""
        filter_values = self._get_filter_values(fdu_filter.get_id())
        if filter_values is None:
            return False
        return label in filter_values

    # TODO : rename method
    def is_system_subject(self):
        return False

    # ----- Access methods -----
    def get_name(self):
        """

        :return: The name of this subject
        """
        # TODO use it everywhere
        return self.title

    def get_id(self):
        """

        :return: Id of this subject
        """
        # TODO use it everywhere
        return self.id

    def get_activated_labels(self, fdu_filter):
        """Returns a structure saying which labels are activated for a filter on this subject

        :param fdu_filter: Filter analyzed
        :return: Structure with label key and value = True if label set, False otherwise
        """
        # Builds a dictionary with labels as keys and False as default value
        labels_activated = dict.fromkeys(fdu_filter.get_labels(), False)
        filter_values = self._get_filter_values(fdu_filter.get_id())
        if filter_values is None:  # If no filtering values was set on this filter
            return labels_activated
        for label in labels_activated.keys():
            if label in filter_values:
                labels_activated[label] = True
        return labels_activated

    def get_subject_informations(self):
        subject_information_url = self._url_builder.subject_information_url(self.subject_type, self.id)
        return self._request_mgr.get_in_python(subject_information_url)

    def print_defined_filtering_values(self):
        """Prints a list of defined filtering values in a subject"""
        subject_information = self._request_mgr.get_in_python(
            self._url_builder.subject_information_url(self.subject_type, self.id))
        print('The filtering values set for the subject', self.get_name())
        # as we will redefine filter values, erase previous ones
        filtering_str = []
        for val in subject_information[self.perimeters_key]:
            filtering_str.append("\tOn filter {}, "
                                 "value(s) defined is/are : {}\n".format(val[self.filter_id_key],
                                                                         val[self.filter_val_key]))
        print("".join(filtering_str))

    def __str__(self):
        type_str = None
        if self.subject_type == "groups":
            type_str = "Group"
        elif self.subject_type == "users":
            type_str = "User"
        return '{} "{}"; id {}'.format(type_str, self.title, self.id)
