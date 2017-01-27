from geodataspace.client.util.dataUtils import UNDEFINED

#######################################
#   Parse geounit command
#   returns  (geounit_name, geounit_id, err_message)
#######################################
def parse_cmd_geounit(cmd_splitted, geounit_id, db):
    cmd_2 = cmd_splitted.get(1, "")
    if cmd_2 == "start":
        geounit_name = cmd_splitted.get(2, UNDEFINED)
        if geounit_name != UNDEFINED:
            return geounit_name, geounit_id, ""
        else:
            return UNDEFINED, None, "cannot understand geounit name"

    elif cmd_2 == "stop":
        pass
        #if geounit_id is None:
        #    return None, None, "cannot use geounit name"

    elif cmd_2 == "delete":
        pass
        #if geounit_id is None:
        #    return None, None, "cannot use geounit name"

    else:
        # geounit something
        return UNDEFINED, None, "usage: geounit [start|stop|delete] <geounit name>"

    return UNDEFINED, None, ""
