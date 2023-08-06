from arcgis.gis import GIS

from orionpy.orioncore.Orion import Orion
from .servicesgismanager import ServicesGISManager


class OrionGIS(Orion):
    def __init__(self, username, password, url_machine, portal="portal", verify_cert=True):
        self._orion = super().__init__(username, password, url_machine, portal, verify_cert)
        portal_url = url_machine + '/' + portal
        self._gis = GIS(portal_url, username, password, verify_cert = verify_cert)
        self._services_gis_mgr = ServicesGISManager(self._gis)

    @property
    def gis(self):
        return self._gis

    @property
    def services_gis_mgr(self):
        return self._services_gis_mgr
