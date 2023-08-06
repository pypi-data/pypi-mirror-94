import csv


class OrionCSV:
    # TODO factorize implementation of read_apply, generate
    def __init__(self, orion):
        self.orion = orion
        self.delimiter = ';'
        self.quoting = csv.QUOTE_MINIMAL
        self.csv_file = None

    def get_csv_writer(self, csv_file, header):
        """Get a csv writer from a given file

        :param header: header of file
        :param csv_file: path to a csv file
        :return: a csv dictionary writer for the given csv file
        """
        return csv.DictWriter(csv_file, fieldnames = header,
                              delimiter = self.delimiter, quoting = self.quoting)

    def get_csv_reader(self, csv_file):
        """Get a csv reader from a given file

        :param csv_file: path to a csv file
        :return: a reader object for the given csv file
        """
        # TODO return a DictReader instead ?
        return csv.reader(csv_file, delimiter = self.delimiter, quoting = self.quoting)

    def _get_groups(self, header, start):
        """Builds list of groups based on csv header"""
        groups = []
        nothing_added = True
        for group_name in header[start:]:
            group = self.orion.groups.get(group_name)
            if group is None:
                print('Group "', group_name, '" does not exist')
            else:
                nothing_added = False
            # To avoid problems later, add value in every cases
            groups.append(group)
        if nothing_added:
            return False
        else:
            return groups
