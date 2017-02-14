from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.datastore.geounit import GeoUnit

#######################################
#   Parse geounit command
#   returns active_geounit object
#######################################
def parse_cmd_geounit(cmd_splitted, active_geounit, geodatamanager):
    cmd_2 = cmd_splitted.get(1, "")
    if cmd_2 == "start":
        new_geounit_name = cmd_splitted.get(2, UNDEFINED)
        if (new_geounit_name == UNDEFINED):
            return active_geounit

        if (active_geounit != None):
            active_geounit.stop()

        active_geounit = GeoUnit(new_geounit_name, geodatamanager)

        if active_geounit is None:
            print "cannot create geounit object"
        else:
            return active_geounit

    elif cmd_2 == "stop":
        if active_geounit is None:
            print "cannot stop: No active geounit"
            return None
        active_geounit.stop()
        return None

    elif cmd_2 == "delete":
        if active_geounit is None:
            print "cannot delete: No active geounit"
            return None
        geodatamanager.delete_geounit(active_geounit.name)
        active_geounit.delete()
        return None

    elif cmd_2 == "list":
        geounits = geodatamanager.get_all_local_geounits()
        print '\n'.join(geounits)
        return active_geounit

    else:
        # geounit something
        print "usage: geounit start <geounit name> (OR) geounit [stop|delete|list] "
        return None
