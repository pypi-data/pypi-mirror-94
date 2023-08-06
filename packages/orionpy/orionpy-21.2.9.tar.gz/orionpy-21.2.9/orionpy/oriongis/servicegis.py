from orionpy.orioncore.resources.Service import Service


class ServiceGIS(Service):
    def __init__(self, service_id, access_url, capabilities, is_hosted=False, is_managed=True):
        super().__init__(service_id, access_url, capabilities, is_hosted, is_managed)
