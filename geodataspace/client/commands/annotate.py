from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected


##########################################################
#   Parse annotatation
#   Annotation is a colon separated key value pair
##########################################################

def parse_cmd_annotate(cmd_splitted, active_geounit):
    if not is_geounit_selected(active_geounit): return

    cmd_2 = cmd_splitted.get(1, "")

    # annotate geounit
    if cmd_2 == "geounit":
        cmd_3 = cmd_splitted.get(2, "")

        if cmd_3 == "add":
            #print "adding annotation to geounit: "
            for key_value in cmd_splitted[3:]:
                property, value = key_value.split(':')
                active_geounit.add_annotation(property, value)

        elif cmd_3 == "delete":
            #print "deleting annotation from geounit: "
            property = cmd_splitted.get(3, "")
            active_geounit.delete_annotation(property)

        else:
            print "wrong usage! try with --annotate geounit [add | delete] [property:value | property]"

    # annotate member
    elif cmd_2 == "member":
        member_name = cmd_splitted.get(2, UNDEFINED)
        if member_name != UNDEFINED and active_geounit.is_member_present(member_name):

            cmd_3 = cmd_splitted.get(3, "")
            if cmd_3 == "add":
                #print "adding annotation to member: " + member_name
                for key_value in cmd_splitted[4:]:
                    property, value = key_value.split(':')
                    active_geounit.add_annotation_to_member(member_name, property, value)

            elif cmd_3 == "delete":
                #print "deleting annotation from member: " + member_name
                property = cmd_splitted.get(4, "")
                active_geounit.delete_annotation_to_member(member_name, property)

            else:
                print "wrong usage! try with --annotate member <member_name> [add | delete] [property:value | property]"

        else:
            print "could not find member: " + member_name

    elif cmd_2 == "list":
        members, properties, values = active_geounit.print_annotations()

    # annotate something
    else:
        print "USAGE: annotate [geounit | member <member name>] [add | delete] [property:value | property]"

