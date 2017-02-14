import os
import re
from geodataspace.client.util.data_utils import UNDEFINED
from geodataspace.client.util.run_utils import is_geounit_selected


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


def parse_cmd_member(cmd_splitted, active_geounit):
    if not is_geounit_selected(active_geounit): return

    cmd_2 = cmd_splitted.get(1, "")

    if cmd_2 == "add":
        member_name = cmd_splitted.get(2, "")
        if os.path.isfile(member_name):
            print "Adding file as a member of this geounit: " + member_name
            active_geounit.add_file(member_name)

        elif os.path.isdir(cmd_2):
            #print "Adding directory as a member of this geounit: " + member_name
            members_list = [dict(data_type="directory", data_uri=os.path.join(cmd_2))]
            for dirname, dirnames, filenames in os.walk(cmd_2):
                for subdirname in dirnames:
                    members_list.append(dict(data_type="directory", data_uri=os.path.join(dirname, subdirname)))
                for filename in filenames:
                    members_list.append(dict(data_type="file", data_uri=os.path.join(dirname, filename)))
                    file_path = os.path.join(dirname, filename)
                    active_geounit.add_file(file_path)

            #TODO: implement files recursive add at directory level
            #print "Adding files: ", str(members_list)
            #active_geounit.add_directory(cmd_2)

        else:
            print "USAGE: member add [<full_file_name> | <folder_path>]"

        print ""


    # delete a member file
    elif cmd_2 == "delete":
        member_name = cmd_splitted.get(2, "")
        if os.path.isfile(member_name) and active_geounit.is_file_present(member_name):
            print "Deleting an already added file of this geounit: " + member_name
            active_geounit.delete_file(member_name)

        else:
            print "cannot find file or folder with name: " + member_name


    # lists all members of this geounit
    elif cmd_2 == "list":
        #members = []
        members = active_geounit.get_members()
        if members == None:
            print "No members are added to current geounit!"
        else:
            print '\n'.join(members)


    # member something
    else:
        print "USAGE: member [add | delete | list] [<file_name> | <folder name>]"


