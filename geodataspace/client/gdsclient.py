__author__ = 'sumanth'

import os, sys

import readline
import atexit

from geodataspace.client.datastore.geodatamanager import GeoDataManager

from geodataspace.client.completer import BufferAwareCompleter
from geodataspace.client.util.data_utils import UNDEFINED, SafeList
from geodataspace.client.util.run_utils import run_command

from geodataspace.client.commands.annotate import parse_cmd_annotate
from geodataspace.client.commands.geounit import parse_cmd_geounit
from geodataspace.client.commands.member import parse_cmd_member
from geodataspace.client.commands.package import parse_cmd_package
from geodataspace.client.commands.track import parse_cmd_track
from geodataspace.client.commands.transfer import parse_cmd_transfer


import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    gdsclient_dir = os.path.join(os.path.expanduser("~"), ".gdsclient")
    if not os.path.exists(gdsclient_dir):
        os.makedirs(gdsclient_dir)

    #create geodatamanager object that manages all geounits locally
    geodatamanager = GeoDataManager(gdsclient_dir)

    #read history from last run
    history_file = geodatamanager.history_file
    try:
        readline.read_history_file(history_file)
    except IOError:
        pass
    atexit.register(readline.write_history_file, history_file)
    del history_file

    #display the suggestions for command auto-completion on pressing the tab button
    cmd_suggestions = geodatamanager.completer_suggestions

    cmd_prefix = '--'
    print ("All gdsclient commands start with  " + cmd_prefix)
    comp = BufferAwareCompleter(cmd_suggestions, cmd_prefix)
    print "Enter --stop to end session"

    readline.set_completer_delims(' \t\n')
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)

    active_geounit = None
    docker_image_id = UNDEFINED
    geounit_name = UNDEFINED

    while True :
        raw_cmd = raw_input(geounit_name + " > ")
        cmd_to_run = raw_cmd.strip()
        cmd_splitted = SafeList(raw_cmd.split())
        first_command = cmd_splitted.get(0, '')

        if first_command.upper() in ['--STOP','--EXIT']:
            break

        elif first_command == "--geounit":
            active_geounit = parse_cmd_geounit(cmd_splitted, active_geounit, geodatamanager)
            if active_geounit != None:
                geounit_name = active_geounit.name
            else:
                geounit_name = UNDEFINED

        elif first_command == "--package":
            new_image_id = parse_cmd_package(cmd_splitted, active_geounit, geodatamanager)
            if new_image_id:
                docker_image_id = new_image_id

        elif first_command in ["--annotate", "--member", "--track"]:
            locals()["parse_cmd_"+first_command[2:]](cmd_splitted, active_geounit)

        elif first_command == "--test":
            parse_cmd_transfer(cmd_splitted, docker_image_id, active_geounit)

        elif first_command == "--transfer":
            parse_cmd_transfer(cmd_splitted, docker_image_id, active_geounit, geodatamanager)

        elif first_command == "cd":
            try:
                os.chdir(cmd_splitted.get(1, os.path.expanduser("~")))
            except Exception as e:
                sys.stderr.write(str(e) + "\n")

        else:
            # any bash command that we want to pass to the system
            run_command(cmd_to_run)
    print "done"
