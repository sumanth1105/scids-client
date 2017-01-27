from geodataspace.client.util.dataUtils import UNDEFINED
from geodataspace.client.catalog.geounit import GeoUnit

#######################################
#   Parse geounit command
#   returns  (active_geounit, geounit_name, err_message)
#######################################
def parse_cmd_geounit(cmd_splitted, user_name, geounit_name, active_geounit, db):
    cmd_2 = cmd_splitted.get(1, "")
    if cmd_2 == "start":
        new_geounit_name = cmd_splitted.get(2, UNDEFINED)
        if (new_geounit_name == UNDEFINED and new_geounit_name == geounit_name):
            return active_geounit, geounit_name, ""

        if (active_geounit != None):
            active_geounit.stop(user_name, geounit_name, db)

        geounit_name = new_geounit_name
        active_geounit = GeoUnit(user_name, geounit_name, db)

        if active_geounit is None:
            return None, UNDEFINED, "cannot create geounit object"
        else:
            return active_geounit, geounit_name, ""

    elif cmd_2 == "stop":
        if active_geounit is None:
            return None, UNDEFINED, "cannot stop: No active geounit"

        active_geounit.stop(user_name, geounit_name, db)
        return None, UNDEFINED, ""

    elif cmd_2 == "delete":
        if active_geounit is None:
            return None, UNDEFINED, "cannot delete: No active geounit"

        active_geounit.delete(user_name, geounit_name, db)
        return None, UNDEFINED, ""

    else:
        # geounit something
        return None, UNDEFINED, "usage: geounit [start|stop|delete] <geounit name>"

    return None, UNDEFINED, ""
