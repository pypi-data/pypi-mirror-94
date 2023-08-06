from orionpy.orioncore.Filter import _FDUFilter
from .orioncsv import OrionCSV


class CSVFilteringValues(OrionCSV):
    # TODO handle labels starting with a 0 !
    def __init__(self, orion):
        super().__init__(orion)
        self.filter_head = 'Filter'
        self.label_head = 'Label'
        self.filter_i = 0
        self.label_i = 1
        self.group_i = 2

    def generate(self, csv_path):
        """Create/Edit a csv file with a summary of all FDU and filtering set for all groups

        :param csv_path: path to the csv files
        """
        print('Generating csv file with a summary of all FDU and filtering values set...')
        # Prepares data and header required
        header = [self.filter_head, self.label_head]
        groups = self.orion.groups.all()
        group_names = []
        for group in groups:
            group_name = group.get_name()
            header.append(group_name)
            group_names.append(group_name)
        filters = self.orion.filters.all_fdu()

        group_labels = dict.fromkeys(group_names, {})

        # TODO factorize following lines with CSVRightsManagement
        try:
            with open(csv_path, "w+", newline = '') as csv_file:
                writer = self.get_csv_writer(csv_file, header)
                writer.writeheader()
                row = {}
                for fdu_filter in filters:
                    # Get the data that interest us (= filtering values and if they're activated)
                    print('\tGetting filtering values for filter "{f}"...'.format(f=fdu_filter.get_name()))
                    for group in groups:
                        group_labels[group.get_name()] = group.get_activated_labels(fdu_filter)
                    # Fills row and write in csv.
                    row[self.filter_head] = fdu_filter.get_name()
                    for label in fdu_filter.get_labels():
                        row[self.label_head] = label
                        for group_name, labels_on in group_labels.items():
                            row[group_name] = '1' if labels_on[label] else '0'
                        writer.writerow(row)
            print('Done ! Csv file containing all filtering values was generated at', csv_path)
        except IOError as e:
            print(e)

    def read_and_apply(self, csv_path):
        """Parse a csv file with fdu, groups and filtering values.
        Does so in order to associate the filtering values in Orion

        :param csv_path: path to the csv files
        """
        print('Scanning file', csv_path, '....')

        fdu_filter = None
        # TODO Call methods using requests (call set_filter_values ?) at the end of the loop
        try:
            with open(csv_path, "r") as csv_file:
                reader = self.get_csv_reader(csv_file)
                # Prepares data
                groups = self._get_groups(header = next(reader), start = self.group_i)
                if not groups:
                    print('None of the group exists..')
                    return

                for row in reader:
                    # If the filter wasn't set or is different from the previous one...
                    if fdu_filter is None or fdu_filter.get_name() != row[self.filter_i]:
                        fdu_filter = self.orion.filters.get(row[self.filter_i])
                        if fdu_filter is None or not isinstance(fdu_filter, _FDUFilter):
                            print('Filter', row[self.filter_i], 'does not exist or not a FDU')
                            continue  # goes to the next line.
                        print('\tAnalyzing filtering values for "{}"...'.format(fdu_filter.get_name()))

                    label = row[self.label_i]
                    if not fdu_filter.is_label_defined(label):
                        print('Label', label, 'not in filter')
                        continue
                    for add_filterval, group in zip(row[self.group_i:], groups):
                        if group is None:  # The group doesn't exist
                            continue
                        # TODO call this at the end (modification for 1 filter of >1 labels)
                        self._change_group_filtering_value(group, fdu_filter, label, add_filterval)
            print('Done ! All possible filtering values were successfully modified !')
        except IOError as e:
            print(e)

    def _change_group_filtering_value(self, group, fdu_filter, label, add_filterval):
        """For a group, add or remove a filtering value based on add_filterval's value"""
        # TODO : just call 'set_filter_values
        if int(add_filterval):  # if the value is different of 0, we must set filtering value
            group.add_filtering_values(fdu_filter, [label])
        else:
            group.remove_filtering_values(fdu_filter, [label])
