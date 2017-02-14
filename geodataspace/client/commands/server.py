import os, re
from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected

#######################################
#   Parse server command
#######################################

def parse_cmd_server(cmd_splitted, docker_image_id, active_geounit):
    if (active_geounit == None): return
