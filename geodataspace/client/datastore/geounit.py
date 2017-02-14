#!/usr/bin/python

import os, sys
import shutil
from leveldb import LevelDB, LevelDBError

from gittle import Gittle
from gittle import GitServer

from geodataspace.client.util.data_utils import UNDEFINED


class GeoUnit:
    repo = None
    annotationsDB = None
    name = UNDEFINED
    repo_name = UNDEFINED
    repo_path = UNDEFINED
    repo_url = UNDEFINED
    user_name = UNDEFINED
    annotationsDB_file = UNDEFINED
    is_active = False

    def __init__(self, geounit_name, geodatamanager):
        if (geounit_name == UNDEFINED):
            return None

        self.name = geounit_name
        self.repo_name = geounit_name
        self.user_name = geodatamanager.user_name
        self.is_active = True

        repo_path = os.path.join(geodatamanager.gdsclient_dir, "repos", geounit_name)
        self.repo_path = repo_path

        db = geodatamanager.levelDb
        is_new_geounit = False
        #print list(db.RangeIter())

        try:
            old_repo_path = db.Get(geounit_name)
            if (old_repo_path != repo_path):
                print "ERROR: Something is messy! Expected path: %s but new path: %s."%old_repo_path %repo_path
        except KeyError:
            is_new_geounit = True

        if (is_new_geounit == True):
            if not os.path.exists(repo_path):
                os.makedirs(repo_path)

            self.repo = Gittle.init(repo_path)
            db.Put(geounit_name, repo_path)
            print "New geounit is created at: %s" %self.repo_path
        else:
            self.repo = Gittle(repo_path)
            print "geounit is already present at: %s" %repo_path

        self.annotationDB_file = os.path.join(repo_path, ".annotationsDB")
        #populate leveldb object from the existing annotations db file
        #if self.annotationsDB == None:
        #    self.annotationsDB = LevelDB(self.annotationsDB_file, create_if_missing=True)
        self.annotationsDB = geodatamanager.levelDb


    def stop(self):
        self.is_active = False


    def delete(self):
        if (self.is_active):
            self.stop()
        self.repo.rm_all()
        try:
            shutil.rmtree(self.repo_path)
        except:
            print "couldn't delete: %s"%self.repo_path

        self.repo = None
        self.repo_name = UNDEFINED
        self.repo_path = UNDEFINED
        self.user_name = UNDEFINED


    def add_file(self, file_name):
        #print "adding file: %s" %file_name
        repo = self.repo
        repo.add(file_name)
        #repo.stage(file_name)
        #repo.commit()
        #print(repo.tracked_files)


    def delete_file(self, file_name):
        #print "deleting file: %s" %file_name
        repo = self.repo
        repo.rm(file_name)
        #repo.commit()
        #print(repo.tracked_files)


    def get_members(self):
        #print "listing all member files in this geounit
        return list(self.repo.tracked_files)


    def is_file_present(self, file_name):
        members = list(self.repo.tracked_files)
        #print members
        for fname in members:
            #print "found the file in current members: " + fname
            if fname == file_name:
                return True

        return False


    def clone(self, repo_name, repo_url):
        print "cloning repo: %s" %repo_name
        repo_path = os.path.join(os.path.expanduser("~"), ".gdsclient", "repos", repo_name)
        repo = Gittle.clone(repo_url, repo_path)
        #repo = Gittle.clone_bare(repo_url, repo_path)


    def commit(self, repo_name):
        print "pushing repo: %s" %repo_name
        repo = self.repo
        #repo.stage(file_name)
        name = "sumanth"
        email = "sumanth1105@github.com"
        message = "test"
        repo.commit(name=name, email=email, message=message)


    def push(self, repo_name):
        print "pushing repo: %s" %repo_name
        repo = self.repo
        #repo.auth(pkey=open("private_key"))
        repo.push()


    def pull(self, repo_name):
        print "pushing repo: %s" %repo_name
        repo = self.repo
        #repo.auth(pkey=open("private_key"))
        repo.pull()


    def print_properties(self, repo_name):
        print "Printing repo properties: %s" %repo_name
        repo = self.repo
        repo.commits
        repo.branches
        repo.modified_files
        repo.abspath(repo_name)
        repo.commit_count()
        repo.tags()
        repo.modified_files
        repo.untracked_files
        repo.tracked_files
        repo.trackable_files
        repo.commit_count()
        repo.diff('HEAD', 'HEAD~1')
        print((list(repo.diff('HEAD'))))
        repo.get_file_versions('./geounit.py')


    def gittle_server_start(self, repo_name):
        print "gittle server for repo: %s" %repo_name
        server = GitServer('/', 'localhost')
        server.serve_forever()


    def add_member(self, member_name):
        print "adding member: %s" %member_name
        repo = self.repo
        repo.add(member_name)


    def is_member_present(self, member_name):
        #print "checking whether %s is present or not." %member
        if os.path.isfile(member_name):
            return self.is_file_present(member_name)

        return False

    '''
    # Adding Annotation has 4 steps:
    1. fetch all the existing annotation tags and create a dictionary of key-value pairs
    2. identify whether this is a new annotation or an update request
    3. remove the older annotation if the key is already present
    4. insert the current annotation as a new git tag
    '''

    def add_annotation(self, property, value):
        print "adding annotation: %s" %property
        if not self.is_active: return

        #create annotations key by appending geounit name as prefix to property
        anndb = self.annotationsDB
        annkey = self.repo_path + ":" + property
        anndb.Put(annkey, value)


    def add_annotation_to_member(self, member_name, property, value):
        print "adding annotation to member: %s"%member_name
        if not self.is_active: return

        #create annotations key by appending geounit name as prefix to property
        anndb = self.annotationsDB
        annkey = member_name + ":" + property
        anndb.Put(annkey, value)


    def delete_annotation(self, property):
        print "deleting annotation: %s" %property
        if not self.is_active: return

        #create annotations key by appending geounit name as prefix to property
        anndb = self.annotationsDB
        annkey = self.repo_path + ":" + property
        try:
            anndb.Delete(annkey)
        except KeyError:
            print "couldn't delete: %s from leveldb file"%property


    def delete_annotation_to_member(self, member_name, property):
        print "deleting annotation to member: %s" %member_name
        if not self.is_active: return

        #create annotations key by appending geounit name as prefix to property
        anndb = self.annotationsDB
        annkey = member_name + ":" + property
        try:
            anndb.Delete(annkey)
        except KeyError:
            print "couldn't delete: %s from leveldb file"%property


    def print_annotations(self):
        if not self.is_active: return

        #create 3 arrays for storing each of the 3 parameters: file_name, property, value
        anndb = self.annotationsDB
        members_list = []
        property_list = []
        values_list = []
        #annotations for all geounits are present in leveldb - check below extraction logic
        for annkey, value in anndb.RangeIter():
            #print(annkey + "  --> " + value)
            #exclude geounit names by checking : in annkey
            if ':' in annkey:
                member, property = annkey.split(':')
                #exclude annotations of other geounits by checking the member scope
                if (member == self.repo_path or self.is_file_present(member)):
                    members_list.append(member)
                    property_list.append(property)
                    values_list.append(value)
                    print(member + " --> " + property + " : " + value)

        return members_list, property_list, values_list

