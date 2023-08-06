from orionpy.orioncore.Filter import _FDUFilter
from .orioncsv import OrionCSV


class CSVOrganisationUnit(OrionCSV):
    # TODO handle labels starting with a 0 !
    def __init__(self, orion, storage_id=""):
        super().__init__(orion)
        self.username_head = 'UserName'
        self.ou_head = 'Organization'
        self.username_i = 0
        self.ou_i = 1
        self.storage_id = storage_id or 'hosted'


    def generate(self, csv_path):
        """Create/Edit a csv file with a summary of all FDU and filtering set for all groups

        :param csv_path: path to the csv files
        """
        print('Generating csv file with a summary of all users and organisational units values set...')
        # Prepares data and header required
        header = [self.username_head, self.ou_head]
        users = self.orion.users.all()

        storage_resource = self.orion.businesses.get_stats_resource(self.storage_id)
        if storage_resource is None:
            print('No stats resource define')
            return None
        
        filter_id = storage_resource.filter_id
        if filter_id is None:
            print('No filter associated with stats resource')
            return None

        rows = []
        for user in users:
            user_id = user.get_id()
            if not user_id.endswith('(default)'):
                user_informations = user.get_subject_informations()
                user_perimeters = user_informations.get('perimeters')
                organization_value = ''
                for perimeter in user_perimeters:
                    if perimeter.get('dimension') == filter_id:
                        organization_value = perimeter.get('valeures')
                        break
                rows.append({
                    self.username_head: user_id, 
                    self.ou_head: organization_value
                })

        # # TODO factorize following lines with CSVRightsManagement
        try:
            with open(csv_path, "w+", encoding='utf8', newline = '') as csv_file:
                writer = self.get_csv_writer(csv_file, header)
                writer.writeheader()
                for row in rows:
                    # Get the data that interest us (= filtering values and if they're activated)
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

        storage_resource = self.orion.businesses.get_stats_resource(self.storage_id)

        if storage_resource is None:
            raise Exception('Storage resource not found: {}'.format(self.storage_id))

        fdu_filter = self.orion.filters.get_with_id(storage_resource.filter_id)

        if storage_resource is None:
            raise Exception('Filter on storage resource not found: {}'.format(storage_resource.filter_id))

        # TODO Call methods using requests (call set_filter_values ?) at the end of the loop
        try:
            with open(csv_path, "r", encoding='utf8') as csv_file:
                reader = self.get_csv_reader(csv_file)
 
                next(reader)
                for row in reader:
                    if len(row) == 0:
                        continue

                    username = row[self.username_i]
                    ou = row[self.ou_i]
                    if not username or not ou:
                        print('\tAssociate user with ou can\'t start because data is missing "username = {}" and "ou = {}"...'.format(username, ou))
                        continue
                    
                    user_id = username
                    if not username.endswith('(agol)'):
                        user_id = username + "(agol)"
                    user = self.orion.users.get_with_id(user_id)

                    if user is None:
                        print('\tUser {} not found '.format(username))
                        continue
                    
                    if not fdu_filter.is_label_defined(ou):
                        print('\tFilter name {} not found '.format(ou))
                        continue

                    filter_values = [ou]
                    user.set_filter_values(fdu_filter, filter_values)

            print('Done ! All possible organisation unit and user association were successfully modified !')
        except IOError as e:
            print(e)
