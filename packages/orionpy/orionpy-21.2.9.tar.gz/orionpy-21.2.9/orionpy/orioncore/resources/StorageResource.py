# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre

import json
from .BusinessResource import BusinessResource


# TODO : factorize with Resource !
class StorageResource(BusinessResource):
    def __init__(self, resource_description):
        """

        :param resource_id: Param _id returned by the REST API
        :param definition: Definition of the cadastre resource
        """
        super().__init__(resource_description)

    @property
    def filter_id(self):
        """
        :return: Associated filter's id
        """
        # TODO get the full filter instead ! (How ?)
        return self._description.get('dimensionId')

    # ----- Activate a filter -----

    def update_filter(self, filter_id):
        """Activates the associated filter for a given group

        :param group: group to activate filter for
        """
        if self.filter_id == filter_id:
            print("The filter is already used for this stats storage")
        else:
            config_url = self._url_builder.stats_configuration_url(self.id)
            
            self._description['dimensionId'] = filter_id
            self._request_mgr.post(config_url, data = {'value': json.dumps(self._description)})
            
            print('Filter', filter_id, 'successfully updated in Stats resource')


    def __str__(self):
        """Provides a string representation of a cadastre resource"""
        resource_str = 'Resource id : {}, ' \
                       'Filtre associé : {}'.format(self.id,
                                                    self.filter_id)
        return resource_str
