import os, re
from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected

#######################################
#   Parse package command
#######################################

def parse_cmd_package(cmd_splitted, active_geounit, geodatamanager):
    if (active_geounit == None): return