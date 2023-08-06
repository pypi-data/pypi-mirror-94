# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre

from .BusinessResource import BusinessResource

# TODO : factorize with Resource !
class StatsResource(BusinessResource):
    def __init__(self, resource_description):
        """

        :param resource_description: Description of the stat resource
        """
        super().__init__(resource_description)



