#!/usr/bin/python
import os, sys

import code
import logging
import readline
import requests
import atexit

import configparser

from leveldb import LevelDB, LevelDBError

from geodataspace.client.datastore.gdsconfig import GDSConfig

from geodataspace.client.completer import BufferAwareCompleter
from geodataspace.client.util.data_utils import UNDEFINED, SafeList
from geodataspace.client.util.run_utils import run_command, is_geounit_selected


import os, sys
import shutil
from geodataspace.client.util.data_utils import UNDEFINED

from gittle import Gittle
from gittle import GitServer

class GeoDataManager:
    cfg = None
    levelDb = None
    completer_suggestions = None
    gdsclient_dir = UNDEFINED
    user_name = UNDEFINED
    leveldb_file = UNDEFINED
    history_file = UNDEFINED

    def __init__(self, gdsclient_dir):

        if not os.path.exists(gdsclient_dir):
            os.makedirs(gdsclient_dir)
        self.gdsclient_dir = gdsclient_dir

        # Read config file
        cfg = GDSConfig(gdsclient_dir)
        self.cfg = cfg
        self.user_name = cfg.get_cfg_field('uname', 'GeoDataspace')

        ## check if the LevelDB local database and history file exists; if not create it;
        ## if exists, reuse the LevelDB local database
        self.levelDB_file = os.path.join(gdsclient_dir, ".gds_levelDB")
        self.history_file = os.path.join(gdsclient_dir, ".gds_history")

        #we have to populate geounits from the locally available list
        #for now hard code the completer suggestions.
        self.completer_suggestions = {
            'geounit':{'start':{}, 'stop':{}, 'delete':{}, 'list':{}},
            'member':{'add':{}, 'delete':{}, 'list':{}},
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
                             {'add':{'property:value':{}, 'property2:value2':{}},
                              'delete':{'property'}},
                         'member':{},
                         'list':{}
                         },
            'stop':{}
        }

        #populate leveldb object from the existing
        db = LevelDB(self.leveldb_file, create_if_missing=True)
        if db == None:
            print("cannot open data from db file: " + self.leveldb_file)
            exit(1)
        self.levelDb = db


    def delete_geounit(self, geounit_name):
        #print "deleting geounit from geodata Manager: %s" %geounit_name
        try:
            repo_path = self.levelDb.Get(geounit_name)
            self.levelDb.Delete(geounit_name)
            print "Successfully deleted geounit from geodata Manager leveldb: %s" %repo_path
        except KeyError:
            print "couldn't delete: %s from leveldb file"%geounit_name


    def get_all_local_geounits(self):
        #print "listing all local geounits in current client: "
        geounits = []
        for key, value in self.levelDb.RangeIter():
            # we don't need annotations in this list
            if not ':' in key:
                geounits.append(key)
        return geounits