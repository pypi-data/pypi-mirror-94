from .Items import Items
from .Geonote import Geonote


class Geonotes(Items):

    def __init__(self):
        super().__init__("Feature Collection", "aob_geonote", lambda data: Geonote(data))
