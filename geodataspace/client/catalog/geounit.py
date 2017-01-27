#!/usr/bin/python

import os, sys
import shutil
from geodataspace.client.util.dataUtils import UNDEFINED

from gittle import Gittle

class GeoUnit:
    repo = None
    repo_name = UNDEFINED
    repo_path = UNDEFINED

    def __init__(self, user_name, geounit_name, db):
        if (geounit_name == UNDEFINED):
            return None
        is_new_geounit = False
        #print list(db.RangeIter())
        try:
            db.Get(geounit_name)
        except KeyError:
            is_new_geounit = True

        if (is_new_geounit == True):
            repo_path = os.path.join(os.path.expanduser("~"), ".gdsclient", "repos", geounit_name)
            if not os.path.exists(repo_path):
                os.makedirs(repo_path)

            self.repo = Gittle.init(repo_path)
            self.repo_name = geounit_name
            self.repo_path = repo_path
            db.Put(geounit_name, repo_path)
            print "New geounit is created at: %s" %self.repo_path
        else:
            print "geounit is already present at: %s" %db.Get(geounit_name)

    def stop(self, user_name, geounit_name, db):
        pass
        #self.repo = None
        #self.repo_name = UNDEFINED
        #self.repo_path = UNDEFINED

    def delete(self, user_name, geounit_name, db):
        try:
            repo_path = db.Get(geounit_name)
            shutil.rmtree(repo_path)
            db.Delete(geounit_name)
        except KeyError:
            print "couldn't delete: %s"%geounit_name
            pass

        self.repo = None
        self.repo_name = UNDEFINED
        self.repo_path = UNDEFINED
