from geodataspace.client.util.dataUtils import UNDEFINED
from geodataspace.client.util.runUtils import is_geounit_selected

#######################################
#   Parse annotatation
#######################################
def parse_cmd_annotate(cmd_splitted, geounit_id, db):
    if not is_geounit_selected(geounit_id): return

    cmd_2 = cmd_splitted.get(1, "")

    # annotate geounit
    if cmd_2 == "geounit":
        print "annotation is for geounit"

    # annotate member
    elif cmd_2 == "member":
        member_name = cmd_splitted.get(2, UNDEFINED)
        if member_name != UNDEFINED:
            print "annotation is for member file"
        else:
            print "please enter the member name: " + member_name

    # annotate something
    else:
        print "USAGE: annotate [geounit |member <member name>] property:value"

