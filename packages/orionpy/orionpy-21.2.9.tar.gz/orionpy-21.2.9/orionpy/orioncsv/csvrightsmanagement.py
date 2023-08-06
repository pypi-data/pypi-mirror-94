from .orioncsv import OrionCSV
from orionpy.orioncore import cfg_global
from orionpy.orioncore.resources.Table import Table
from orionpy.orioncore.resources.Field import Field
from orionpy.orioncore.resources.Layer import Layer
from orionpy.orioncore.resources.Resource import RightLevel
from orionpy.orioncore.resources.Service import Service


class CSVRightsManagement(OrionCSV):
    def __init__(self, oriongis):
        super().__init__(oriongis)
        self.type_head = 'Type'
        self.url_head = 'Relative url'
        self.label_head = 'Label'
        # TODO also use dictionary value instead of indexes.
        self.type_i = 0
        self.url_i = 1
        self.label_i = 2
        self.inherited_val = 'inherited'

    def generate(self, csv_path, service, group_list=None):
        """Create/Edit a csv file with a summary of all group rights on a service and its components
        (fields, layers, tables, ...)

        :param csv_path: path to the csv files
        :param service: The service for which we want a summary of rights
        :param group_list: (TEMPORARY) groups for which we want rights
        """
        # TODO improve performances !
        if not self._is_service_valid(service):
            return
        print('Generating csv file with a summary of rights for the', service, '...')
        # Builds the header
        header = [self.type_head, self.url_head, self.label_head]

        # If group_list not set, get groups for which service is shared with
        if group_list is None or not group_list:
            group_list = []
            if not cfg_global.is_federated:
                # group_list = self.orion.groups.all()
                print('Not able to get groups if not federated')
                return
            else:
                # TODO how to test if is of OrionGIS type ?
                # if not isinstance(self.orion, OrionGIS) :
                #     print('if you do not use OrionGIS, please specify a list of group !')
                #     return
                groups_ids = self.orion.services_gis_mgr.get_groups_id_shared(service = service)
                for group_id in groups_ids:
                    group_list.append(self.orion.groups.get_with_id(group_id))
        groups = self._add_groups_header(group_list, header)
        if not groups:
            print('None of the group exists..')
            return

        try:
            with open(csv_path, "w+", newline = '') as csv_file:
                writer = self.get_csv_writer(csv_file, header)
                writer.writeheader()
                self._write_resource_information(writer, service, group_list)

                for layer in service.layers.all():
                    print('\tGetting rights for layer "{}"...'.format(layer.get_name()))
                    self._write_resource_information(writer, layer, group_list)
                    for field in layer.fields.all():
                        print('\t\tGetting rights for field "{}"...'.format(field.get_name()))
                        self._write_resource_information(writer, field, group_list)

                for table in service.tables.all():
                    print('\tGetting rights for table "{}"...'.format(table.get_name()))
                    self._write_resource_information(writer, table, group_list)
                    for field in table.fields.all():
                        print('\t\tGetting rights for field "{}"...'.format(field.get_name()))
                        self._write_resource_information(writer, field, group_list)

            print('Done ! Csv file containing rights on resource was generated at', csv_path)
        except IOError as e:
            print(e)

    def _is_service_valid(self, service):
        """Test if can generate a csv of rights on a service

        :param service: The service concerned
        :return: True if there is no problem with the service, False otherwise.
        """
        if service is None:
            print('Service does not exist')
            return False
        if cfg_global.is_federated and not service.is_managed():
            print('Service must be managed by aOB to generate a summary of rights')
            return False
        return True

    def _add_groups_header(self, group_list, header):
        """Adds a grouplist to the header"""
        groups_remaining = False
        for group in group_list:
            if group is not None:
                header.append(group.get_name())
                groups_remaining = True
        if not groups_remaining:
            print('No group to get')
            return False
        return group_list

    def _write_resource_information(self, writer, resource, group_list):
        """Writes one resource rights

        :param writer: the csv writer
        :param resource: resource concerned
        :param group_list: groups for which write information
        """
        row_dict = {self.type_head: resource.get_type(),
                    self.url_head: resource.get_access_url(),
                    self.label_head: resource.get_name()}
        for group in group_list:
            if group is not None:
                right = resource.get_resolved_right(group).value

                if resource.has_inherited_right(group):
                    row_dict[group.get_name()] = "{} ({})".format(self.inherited_val, right)
                else:
                    row_dict[group.get_name()] = right
        writer.writerow(row_dict)

    def read_and_apply(self, csv_path, handle_sharing=False):
        """Parse a csv file with resources, groups and rights.
        Does so in order to update rights for groups

        :param csv_path: path to the csv files
        :param handle_sharing: Boolean saying if handle sharing with groups or not
        """
        print('Scanning file', csv_path, '....')
        dic_resource = {Service.get_type(): None,
                        Layer.get_type(): None,
                        Table.get_type(): None}
        try:
            with open(csv_path, "r") as csv_file:
                # TODO use DictReader ?
                reader = self.get_csv_reader(csv_file)
                # Prepares data
                groups = self._get_groups(header = next(reader), start = 3)
                if not groups:
                    print('None of the group exists..')
                    return

                sharing_checked = False
                # Get data for each row and, if possible, update right
                for row in reader:
                    resource = self._get_correct_resource(row, dic_resource)
                    if handle_sharing and not sharing_checked and \
                            dic_resource[Service.get_type()] is not None:
                        self._handle_sharing(dic_resource[Service.get_type()], groups)
                        sharing_checked = True  # avoid calling this method a million time
                    if resource is None:
                        continue
                    # TODO reduce number of calls to update if not needed.
                    self._update_resource_right(resource, row, groups)
            print('Done ! All possible rights values were successfully updated !')
        except IOError as e:
            print(e)

    def _handle_sharing(self, service, groups):
        """ If service not shared w/ group, share it with it"""
        for group in groups:
            if group is not None and \
                    not self.orion.services_gis_mgr.is_shared_with(service, group.get_id()):
                self.orion.services_gis_mgr.share(service, group.get_id())

    def _get_correct_resource(self, row, resource_d):
        """Based on type in row and resources got before, return correct resource

        :return: Resource or None if problem getting resource"""
        if row[self.type_i] == Service.get_type():
            resource_d[Service.get_type()] = self.orion.services.get_in_managed(row[self.url_i])
            return resource_d[Service.get_type()]
        elif row[self.type_i] == Layer.get_type() and resource_d[Service.get_type()] is not None:
            # Get layer's id from REST url.
            layer_id = row[self.url_i].split('/')[-1]
            resource_d[Layer.get_type()] = resource_d[Service.get_type()].layers.get_with_id(
                layer_id)
            return resource_d[Layer.get_type()]
        elif row[self.type_i] == Table.get_type() and resource_d[Service.get_type()] is not None:
            resource_d[Layer.get_type()] = None  # for field's right handling
            table_id = row[self.url_i].split('/')[-1]
            resource_d[Table.get_type()] = resource_d[Service.get_type()].tables.get_with_id(
                table_id)
            return resource_d[Table.get_type()]
        elif row[self.type_i] == Field.get_type():
            # Get field's name from REST url.
            field_name = row[self.url_i].split('/')[-1]
            # NB : no need to save field in this case
            if resource_d[Layer.get_type()] is not None:
                return resource_d[Layer.get_type()].fields.get(field_name)
            elif resource_d[Table.get_type()] is not None:
                return resource_d[Table.get_type()].fields.get(field_name)
        print('Unknown type', row[self.type_i])
        return None

    def _update_resource_right(self, resource, row, groups):
        """Check and update a resource's right for each group of groups."""
        if resource is None:
            print('Resource', row[1:3], 'unknown')
            return
        for val, group in zip(row[3:], groups):
            if group is None:  # The group doesn't exist
                continue
            self._update_good_right(val, group, resource)

    def _update_good_right(self, val, group, resource):
        """Calls the good update_right method based on val"""
        val = val.strip()  # handle trailing blanklines
        right = None
        # If empty string read, treated the same way as 'inherited'
        if val.startswith(self.inherited_val) or not val:
            resource.enable_inheritance(group)
            return

        # TODO "pythonic switch" ? Or get_enum_from_value method ?
        if val == RightLevel.ACCESS.value:
            right = RightLevel.ACCESS
        elif val == RightLevel.READ.value:
            right = RightLevel.READ
        elif val == RightLevel.WRITE.value:
            right = RightLevel.WRITE
        else:
            print('ERROR : wrong right type "', val, '" in csv')
            return
        resource.force_right(group, right)
