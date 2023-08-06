from orionpy.orioncsv import orioncsv
import json


class CSVFilteringCadastre(orioncsv.OrionCSV):
    def __init__(self, orion):
        super().__init__(orion)
        self.orion = orion
        self.group = "group"
        self.right = "role"
        self.filter_values = "scope"
        self.group_i = 0
        self.right_i = 1
        self.filter_values_i = 2

    def generate(self, csv_path, json_path):
        """Generate a csv file with the groups, the rights and
        the filter values, ready to import

        :param csv_path: path of the csv file you want to generate
        :param json_path: path of the json file where the data is stored
        """
        self._csv_process(csv_path, self._json_extract_information(json_path))

    def _init_generate(self, json_path):
        """Generate a dictionnary from

        :param json_path: path of the json file where the data is stored
        :return: Dictionary of needed values to update the rights
        """
        with open(json_path, 'r', encoding="utf-8") as json_data:
            data_list_input = json.load(json_data)
            data_dict_input = data_list_input[0]
        profiles_dict = data_dict_input["profiles"]
        return profiles_dict

    def _json_extract_information(self, json_path):
        """Extract the needed informations from the json file

        :param json_path: path of the json file where the data is stored
        :return: A list of dict with json needed informations included. List : [group, role, scope].
        """
        data_list_output = list()
        profiles_dict = self._init_generate(json_path)

        for dictionary in profiles_dict:
            temp_dict = dict()
            if self.group in dictionary.keys():
                temp_dict[self.group] = dictionary[self.group]
            if "rules" in dictionary.keys():
                sub_set = set()
                for sub_dico in dictionary["rules"]:
                    self._add_right_or_filter_values(sub_dico, temp_dict, sub_set)
                temp_dict[self.filter_values] = sub_set
                if self.right not in temp_dict.keys():
                    temp_dict[self.right] = "public"  # if there is no "right" defined, public
            data_list_output.append(temp_dict)
        return data_list_output

    def _add_right_or_filter_values(self, sub_dico, temp_dict, sub_set):
        """Add right or filter values

        :param sub_dico:
        :param temp_dict:
        :param sub_set:
        """
        if self.right in sub_dico.keys():
            temp_dict[self.right] = sub_dico[self.right]
        elif self.filter_values in sub_dico.keys():
            sub_set.add(sub_dico[self.filter_values])

    def _csv_process(self, csv_path, data_list):
        """Create the CSV with the data list

        :param csv_path: path of the csv file you want to generate
        :param data_list: json informations extracted in a list of dict
        """
        csvfile = open(csv_path, 'w', newline='')
        first_line = [self.group, self.right, self.filter_values]
        writer = self.get_csv_writer(csvfile, first_line)
        writer.writeheader()
        for dico in data_list:
            group = dico[self.group]
            role = dico[self.right]
            if role == set():
                role = ''
            scope = ''
            if scope != set():
                for element in dico[self.filter_values]:
                    scope += str(element) + ','
                scope = scope[:-1]
            writer.writerow({self.group: group, self.right: role, self.filter_values: scope})
        csvfile.close()

    def read_and_apply(self, csv_path):
        """Parse the csv file and apply the rights on aOB

        :param csv_path: path of the csv file
        """
        cadastre_resource = self.orion.services.get_cadastre_resource()
        fdu_filter = self.orion.filters.get_with_id(cadastre_resource.associated_filter_id)
        cadastre_resource.init_filter_access(fdu_filter)
        csv_file = open(csv_path, 'r', encoding="utf-8")
        csv_reader = self.get_csv_reader(csv_file)
        field = "id_comm"
        next(csv_reader)
        line_count = 1
        for row in csv_reader:
            print("\n", row,"\n")
            line_count += 1
            group = self.orion.groups.get(row[self.group_i])
            if group == None:
                print("The line ", line_count, " ( group : \"",row[self.group_i] ,"\" ) of the CSV will not be used, due "
                        "to an error. Please check the group name in the CSV or check if the group is define on aOB")
                continue
            filter_values = list(filter(lambda value: value != "", row[self.filter_values_i].split(','))) # make a list of filter values
            self._set_filter_values(group, fdu_filter, filter_values, field, row[self.right_i])
            if not cadastre_resource.update_right_from_string(group, row[self.right_i]):
                print("The line ", line_count, " ( group : \"",row[self.group_i] ,"\" ) of the CSV will not be used, due "
                                                                    "to an error. Please check the right in the CSV.")
                continue
            self._activate_or_deactivate_filter(row, group, filter_values, cadastre_resource)

    def _activate_or_deactivate_filter(self, row, group, filter_values, cadastre_resource):
        """Determine if the filter needs to be activated / deactivated

        :param row:
        :param group:
        :param filter_values:
        :param cadastre_resource:
        """
        if row[self.right_i] == "public" and filter_values:
            cadastre_resource.activate_filter(group)
        elif row[self.right_i] == "public" and not filter_values:
            cadastre_resource.deactivate_filter(group)

    def _set_filter_values(self, group, fdu_filter, filter_values, field, right_string):
        """Set the filter values / particular case with no values and nominative access

        :param group:
        :param fdu_filter:
        :param filter_values:
        :param field:
        :param right_string:
        """
        if right_string == 'nominatif' and not filter_values:
            group.set_filter_values(fdu_filter, add_all_values=True)
        else:
            group.set_filter_field_values(fdu_filter, filter_values, field)
