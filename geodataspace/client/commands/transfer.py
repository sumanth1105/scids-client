import os, re
from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected

#######################################
#   Parse transfer command
#######################################

def parse_cmd_transfer(cmd_splitted, docker_image_id, active_geounit, geodatamanager):
    if (active_geounit == None): return
