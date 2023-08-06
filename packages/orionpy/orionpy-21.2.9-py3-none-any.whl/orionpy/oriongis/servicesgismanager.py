from orionpy.orioncore.resources.Services import Services
from orionpy.orioncore import cfg_global


# https://front.arcopole.fr/Orion/orion/admin/tree/object/SERVICES/Cannes/EspacesVerts_FeatureServer/__refreshPortalItemSharingData
# GET
# f & token

class ServicesGISManager(Services):
    def __init__(self, gis):
        super().__init__()
        self._gis = gis

    def get_gis(self, element_id):
        service = super().get(element_id)
        return self._gis.content.get(service.id)  # arcgis

    def share(self, service, group_id):
        """Shares a given service with a given group"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        if self.is_shared_with(service, group_id):
            print('Service', service.get_access_url(), 'already shared with group', group_id)
            return
        service_arcgis = self._gis.content.get(service.id)
        print(service_arcgis.share(groups = group_id))

    def unshare(self, service, group_id):
        """Unshares a given service with a given group"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        if not self.is_shared_with(service, group_id):
            print('Service', service.get_access_url(), 'already not shared with group', group_id)
            return
        service_arcgis = self._gis.content.get(service.id)
        print(service_arcgis.unshare(groups = group_id))

    def get_groups_id_shared(self, service):
        """Get the list of groups'ids where service is shared with"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        service_arcgis = self._gis.content.get(service.id)
        url = self.url_manager.resource_sharing_url(service_arcgis.id,
                                                    service_arcgis.owner)
        req = self.request.post_in_python(url)
        groups_ids = req['sharing']['groups']
        if req['sharing']['access'] == 'org':
            groups_ids.append('org')
        elif req['sharing']['access'] == 'public':
            groups_ids.append('public')
            groups_ids.append('org')

        return groups_ids

    def is_shared_with(self, service, group_id):
        """Check if a given group is shared with a service"""
        if not cfg_global.is_federated:
            print('Method not available if ArcGIS not federated')
            return
        groups_ids = self.get_groups_id_shared(service)
        for group_ids in groups_ids:
            if group_id == group_ids:
                return True
        return False
