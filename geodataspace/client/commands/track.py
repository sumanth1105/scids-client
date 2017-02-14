import os, re
from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected

#######################################
#   Parse track command
#######################################

def parse_cmd_track(cmd_splitted, geounit):
    if (geounit == None): return
