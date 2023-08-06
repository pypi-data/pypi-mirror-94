# ---- Get informations about a group----
# https://{machine}/{api}/rightmanagement/groups/{group}
# GET
# f & token

# ---- Get rights on resources ----
# https://{machine}/{api}/rightmanagement/groups/{group}/authorizedResources

# ---- Get rights on services ----
# {getRightsResources_URL}/SERVICES

# ---- Get right on a particular service ----
# {getRightServices_URL}/{service}

# ---- Get rights on a layer ----
# {getRightsParticularService_URL}/{layer}

# ---- Get rights on a field ----
# {getRightsLayer_URL}/{field}

# ---- Set filtering values ----
# {groupInformationURL}/__configure
# value = {"name":$GROUP_ID$,
#          "domaine":$GROUP_DOMAIN$,
#          "perimeters":
#               [{"dimension":$FILTER_ID$,
#                 "valeures":$ONE_SELECTED_FILTERING_VAL$
#                 }*
#                ]
#         }
# https://{machine}/{api}/rightmanagement/groups/{group}
#    {
#     "title":"Organisation",
#     "name":"org",
#     "domain":"default",
#     "isSuperAdmin":false,
#     "perimeters": # defined filtering values
#      [
#      ],
#     "properties":
#      {
#       "builtinRole":"authenticated"
#      }
#    }

# "name": "128703724fce49358406f2dfcf8d43aa",
# "nodeType": "GroupNode",
# "title": "Accueil"

import json

from .Subject import Subject


class User(Subject):
    """Single group-data handling class"""

    def __init__(self, title, user_id, profile_id = None):
        super().__init__(title, user_id, "users", profile_id)
