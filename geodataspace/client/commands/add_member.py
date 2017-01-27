import os
import re
from geodataspace.client.util.dataUtils import UNDEFINED
from geodataspace.client.util.runUtils import is_geounit_selected

#######################################
#   Parse add_member command
#######################################
def cmd_count_files(process):
    cnt_files = 0
    for line in iter(process.stdout.readline, ''):
        matches = re.search("(.*) <(\d*)> .*", line.strip())
        if matches is not None:
            member_name = matches.group(1)
            member_id = matches.group(2)
            cnt_files += 1
            print "   > ", member_name," with id ", member_id
    return cnt_files

def parse_cmd_add_member(cmd_splitted, geounit_id, db):
    if not is_geounit_selected(geounit_id): return

    cmd_2 = cmd_splitted.get(1, "")
    if cmd_2 == "":
        print "USAGE: add_member [<file_name> | <folder name>]"

    # add file as a member
    elif os.path.isfile(cmd_2):
        print "Adding file as a member of this geounit: " + cmd_2
        pass

    # add members from folder
    elif os.path.isdir(cmd_2):

        members_list = [dict(data_type="directory", data_uri=os.path.join(cmd_2))]
        for dirname, dirnames, filenames in os.walk(cmd_2):
            for subdirname in dirnames:
                members_list.append(dict(data_type="directory", data_uri=os.path.join(dirname, subdirname)))
            for filename in filenames:
                members_list.append(dict(data_type="file", data_uri=os.path.join(dirname, filename)))

        print "Adding: ", str(members_list)
        pass

    # add_member something
    else:
        print "cannot find file or folder with name " + cmd_2

