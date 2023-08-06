# **** Get the list of all filters ****
#  https://front.arcopole.fr/Orion/orion/admin/tree/config/dimensions
# GET
# f & token

#  **** Creation/Edition/Duplication/Deletion of a new filter ****
#  https://front.arcopole.fr/Orion/orion/admin/tree/config/dimensions/__configure
# GET (create)
# f & token & value = list of all filters plus the one added
# For creation, the one added doesn't have the id & dbId fields set & partitions is empty

# **** Configuration des valeurs de filtrage ****
# https://front.arcopole.fr/Orion/orion/admin/tree/rightmanagement/groups/$GROUP_ID$/__configure
# GET
# f & token &
# value = {"name":$GROUP_ID$,
#           "domaine":$GROUP_DOMAIN$,
#           "perimeters":
#                       [{"dimension":$FILTER_ID$,
#                         "valeures":$ONE_SELECTED_FILTERING_VAL$
#                        }*
#                       ]
#         }
from .Exceptions import BuildFilterError


class FilterFactory:
    # TODO figure out what to do if dic AND parameters given
    # TODO is class really useful ?...
    # TODO Abstract factory ?
    """The Factory for our filter.

    Create a Filter of SQL or FDU type based on the arguments given.
    e.g. if the whereClause is given, then this might be a SQL filter
    """

    @staticmethod
    def try_to_build_sql(name, where_clause, filter_dic):
        """Internal function. Check if parameters to build a sql filter are good.
        If that's the case, build a SQL filter

        :return: the Filter built or None if nothing was built
        :raises BuildFilterError: if name or whereClause is empty
        """
        if filter_dic is not None \
                and "whereClause" in filter_dic and filter_dic['whereClause']:
            return _SQLFilter(filter_dic['name'].strip(), filter_dic['whereClause'].strip(),
                              filter_dic)
        if name is not None and where_clause is not None:
            if name.strip() and where_clause.strip():  # name and whereClause aren't empty
                return _SQLFilter(name.strip(), where_clause.strip())
            else:
                raise BuildFilterError(
                    "[ERROR SQL Filter] name and whereClause must not be empty")
        return None

    @staticmethod
    def try_to_build_fdu(name, attributes, properties, filtering_values, filter_dic):
        """Internal function. Check if parameters to build a FDU filter are good.
        If that's the case, build a FDU filter

        :return: the Filter built or None if nothing was built
        :raises: BuildFilterError if name or attributeName or partition is empty
        """
        if filter_dic is not None and "attributeName" in filter_dic:
            return _FDUFilter(filter_dic['name'], filter_dic['attributeName'],
                              filter_dic['properties'], filter_dic['partitions'],
                              filter_dic)
        if name is not None and attributes is not None and filtering_values is not None:
            if name.strip() and attributes and filtering_values:
                return _FDUFilter(name.strip(), attributes, properties, filtering_values)
            else:
                raise BuildFilterError(
                    "[ERROR FDU] name, attributeName and filtering_values must not be empty")
        return None

    def build_filter(name=None, attributes=None, properties=None, filtering_values=None,
                     where_clause=None, filter_dic=None, filter_type=None):
        # TODO Improve this method !
        """
        :param where_clause:
        :param filtering_values:
        :param properties:
        :param attributes:
        :param name:
        :param filter_dic: Alternative construction. Dictionary containing all parameters
        :param filter_type: Type of filter required (sql or fdu)
        :return: the Filter built or None if there was a problem during construction
        """
        try:
            if filter_type is not None:
                if filter_type != 'sql' and filter_type != 'fdu':
                    raise BuildFilterError("[ERROR Filter] invalid type_filt.", filter_type,
                                           "must be 'fdu' or 'sql'")
                if filter_type == 'sql':
                    return FilterFactory.try_to_build_sql(name, where_clause, filter_dic)
                if filter_type == 'fdu':
                    return FilterFactory.try_to_build_fdu(name, attributes, properties,
                                                          filtering_values, filter_dic)
            else:
                new_filter = FilterFactory.try_to_build_sql(name, where_clause, filter_dic)
                if new_filter is None:
                    new_filter = FilterFactory.try_to_build_fdu(name, attributes, properties,
                                                                filtering_values, filter_dic)
                    if new_filter is None:
                        raise BuildFilterError(
                            "[ERROR FILTER] Problem in arguments, no filter built")
        except BuildFilterError as e:
            print(e.args)
            new_filter = None
        return new_filter

    build_filter = staticmethod(build_filter)


class Filter:
    # TODO private class ?
    def __init__(self, name=None, filter_dic=None, filter_id=None):
        """Create a generic filter

        :param name: Filter name
        :param filter_id: Filter id
        :param filter_dic: A dictionary that containing filter's parameters
        """
        if filter_dic is not None:
            self.name = filter_dic['name']
            self.id = filter_dic['id']
            if "dbID" in filter_dic:
                self.db_id = filter_dic['dbId']
        else:
            self.name = name
            self.id = filter_id

    def get_id(self):
        """ Returns filter's id """
        if self.id is not None:
            return self.id
        else:
            print('No id set for this filter')
            return None

    def get_name(self):
        return self.name

    def __str__(self):
        """Allows to have a string representation of a filter to print.

        :return: the string representation of a filter.
        """
        return 'Filter {}; id {}'.format(self.name, self.id)


class _SQLFilter(Filter):
    """SQLFilter. A specific type of filter with a sql where request.
    SQL Filter can be applied only to a layer or a table (not a service)
    """

    def __init__(self, name="", whereClause="", filter_dic=None, filter_id=None):
        super(_SQLFilter, self).__init__(name = name,
                                         filter_dic = filter_dic,
                                         filter_id = filter_id)
        if filter_dic is not None:
            self.whereClause = filter_dic['whereClause'].strip()
        else:
            self.whereClause = whereClause.strip()

    def __str__(self):
        filter_str = ['SQL Filter "{name}"; whereClause : {wc}'.format(name = self.name,
                                                                       wc = self.whereClause)]
        if self.id is not None:
            filter_str.append("; id {}".format(self.id))
        return "".join(filter_str)


class _FDUFilter(Filter):
    """
    A filter depending on the user. Applied on some specific values of attributes.
    Can be applied only if fields of the filter are in the layer/table selected
    Can be applied on a layer only if applied on the corresponding service/table
     {
      "name":$FILTER_NAME$,
      "id": $ID$,
      "dbId":$DB_ID$,
      "attributeName":
       [
          [$fieldName$]+
       ],
      "properties":null,
      "partitions":
       [
          [{
           "name":$name$,
           "properties":
            {
             [$label$: $associatedValue$]+
            }
          }]+
       ],
      "whereClause":null
     },
    """

    def __init__(self, name, attributeName, properties=None,
                 partitions=None, filter_dic=None, filter_id=None):
        """
        :param attributeName: Field(s) concerned by the filter
        :param properties: ??
        :param partitions: valeurs de filtrage. List of value(s) selected for the field
        """
        super(_FDUFilter, self).__init__(name = name, filter_dic = filter_dic,
                                         filter_id = filter_id)

        if filter_dic is not None:
            self.attributeName = filter_dic['attributeName']
            self.properties = filter_dic['properties']
            self.partitions = filter_dic['partitions']
        else:
            self.attributeName = attributeName
            self.partitions = partitions
            self.properties = properties

    def is_label_defined(self, label):
        """Check if a given filtering value's label is defined for this FDU

        :param label: the label to look for
        :return: True if the label was found, False otherwise
        """
        label = label.strip()
        for filtering_value in self.partitions:
            if filtering_value['name'] == label:
                return True
        return False

    def is_field_value_defined(self, field, value):
        """Check if a given filtering value as the field value for this FDU

        :param field: Field with value to look for
        :param value: Value to check if defined
        :return: True if the field value is defined. False otherwitse
        """
        if field not in self.get_fields():
            return False
        for filtering_value in self.partitions:
            if filtering_value['properties'][field] == value:
                return True
        return False

    def get_labels_for(self, field, value):
        """Get labels for filtering values including the field value.

        :param field: Field with value to look for
        :param value: Value to get labels for
        :return: Array with labels having this field value
        """
        if field not in self.get_fields():
            return []
        labels = []
        for filtering_value in self.partitions:
            if filtering_value['properties'][field] == value:
                labels.append(filtering_value['name'])
        return labels

    def get_fields(self):
        """
        :return: Fields concerned by the filter"""
        return self.attributeName

    def get_labels(self):
        """Return all labels corresponding to FDU's filtering values

        :return: List of labels or an empty list if there's no defined labels
        """
        labels_list = []
        for filtering_value in self.partitions:
            labels_list.append(filtering_value['name'])
        return labels_list

    def __str__(self):
        """
        :return: A string representation of the FDU filter
        """
        filter_str = ['FDU Filter "{}"; attribute name(s): {};'.format(self.name,
                                                                       self.attributeName),
                      "\n\tFiltering values = "]
        for filter_val in self.partitions:
            filter_str.append('label:' + filter_val['name'] + '; ')
            for attr in self.attributeName[:-1]:
                filter_str.append('values:' + filter_val['properties'][attr] + ', ')
            if len(self.attributeName) == 1:
                filter_str.append('value:')
            filter_str.append(filter_val['properties'][self.attributeName[-1]] + '; ')
        if self.id is not None:
            filter_str.append("id {}".format(self.id))
        return "".join(filter_str)
