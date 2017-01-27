from geodataspace.client.util.dataUtils import UNDEFINED
from geodataspace.client.util.runUtils import is_geounit_selected

#######################################
#   Parse annotatation
#######################################
def parse_cmd_annotate(cmd_splitted, active_geounit, db):
    if not is_geounit_selected(active_geounit): return

    cmd_2 = cmd_splitted.get(1, "")

    # annotate geounit
    if cmd_2 == "geounit":
        print "annotation is for geounit"
        for geo_prop_value in cmd_splitted[2:]:
            prop, value = geo_prop_value.split(':')
            print "Annotation: %s" %geo_prop_value
            active_geounit.add_annotation(prop, value)

    # annotate member
    elif cmd_2 == "member":
        member_name = cmd_splitted.get(2, UNDEFINED)
        if member_name != UNDEFINED:
            print "annotation is for member file"
            if active_geounit.is_member_present(member_name):
                for member_prop_value in cmd_splitted[3:]:
                    prop, value = member_prop_value.split(':')
                    print "Annotation: %s" %member_prop_value
                    active_geounit.add_annotation_to_member(member_name, prop, value) 
        else:
            print "Member is not present: " + member_name

    # annotate something
    else:
        print "USAGE: annotate [geounit |member <member name>] property:value"

