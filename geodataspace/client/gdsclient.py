__author__ = 'sumanth'

import os, sys

import code
import logging
import readline
import requests
import atexit

import configparser

from leveldb import LevelDB, LevelDBError

from geodataspace.client.catalog.gdsconfig import GDSConfig

from geodataspace.client.completer import BufferAwareCompleter
from geodataspace.client.util.dataUtils import UNDEFINED, SafeList
from geodataspace.client.util.runUtils import run_command, is_geounit_selected

from geodataspace.client.commands.geounit import parse_cmd_geounit
from geodataspace.client.commands.annotate import parse_cmd_annotate
from geodataspace.client.commands.add_member import parse_cmd_add_member

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    gdsclientdir = os.path.join(os.path.expanduser("~"), ".gdsclient")
    if not os.path.exists(gdsclientdir):
        os.makedirs(gdsclientdir)

    # Read config file
    cfg = GDSConfig()
    user_name = cfg.get_cfg_field('uname', 'GeoDataspace')

    ## check if the LevelDB local database and history file exists; if not create it;	
    ## if exists, reuse the LevelDB local database
    levelDB_file = os.path.join(gdsclientdir, ".gds_levelDB")
    history_file = os.path.join(gdsclientdir, ".gds_history")
    try:
        readline.read_history_file(history_file)
    except IOError:
        pass
    atexit.register(readline.write_history_file, history_file)
    del history_file

    db = LevelDB(levelDB_file, create_if_missing=True)
    if db == None:
        print("cannot open data from db file: " + levelDB_file)
        exit(1)

    print "enter --stop to end session"

    completer_suggestions = {
        'geounit':{'start':{}, 'stop':{}, 'delete':{}},
        'add_member':{},
        'track':{},
        'transfer':{},
        'package':{'provenance':
                         {'level':{'individual':{}, 'collaboration':{}, 'community':{}}
                          },
                     'level':{'individual':{}, 'collaboration':{}, 'community':{}},
                     'list':{},
                     'add':{},
                     'delete':{},
                     },
        'annotate':{'geounit':
                         {'geoprop1':{}, 'prop2':{}, 'fluid':{}
                          },
                     'member':{}
                     },
        'stop':{}
    }

    gds_client_special_string = '--'
    print ("All gdsclient commands start with  " + gds_client_special_string)
    comp = BufferAwareCompleter(completer_suggestions, gds_client_special_string)

    readline.set_completer_delims(' \t\n')
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)

    active_geounit = None
    geounit_name = UNDEFINED

    while True :
        raw_cmd = raw_input(geounit_name + " > ")
        cmd_to_run = raw_cmd.strip()
        cmd_splitted = SafeList(raw_cmd.split())
        first_command = cmd_splitted.get(0, '')

        if first_command.upper() in ['--STOP','--EXIT']:
            break

        elif first_command == "--geounit":
            active_geounit, geounit_name, err_message = parse_cmd_geounit(cmd_splitted, user_name, geounit_name, active_geounit, db)
            if err_message != "":
                print err_message

        elif first_command in ["--annotate", "--add_member"]:
            locals()["parse_cmd_"+first_command[2:]](cmd_splitted, active_geounit, db)

        elif first_command == "cd":
            try:
                os.chdir(cmd_splitted.get(1, os.path.expanduser("~")))
            except Exception as e:
                sys.stderr.write(str(e) + "\n")

        else:
            # any bash command that we want to pass to the system
            run_command(cmd_to_run)
    print "done"
