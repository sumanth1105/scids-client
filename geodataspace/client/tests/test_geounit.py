#!/usr/bin/python

import os, sys, re

from geodataspace.client.datastore.geodatamanager import GeoDataManager
from geodataspace.client.datastore.geounit import GeoUnit

def test_new_geounit():
    gdsclient_dir = '/tmp/gdsclient/'
    geodatamanger = GeoDataManager(gdsclient_dir)
    geounit_name = 'test'

    g = GeoUnit(geounit_name, geodatamanger)
    file_path = '/Users/Rajeevm/sumanth/DePaul/work/test/sample'
    g.add_file(file_path)


    repo = g.repo
    #repo.stage(file_path)
    repo.add(file_path)

    name = 'sumanth'
    email = 'sumanth1105@github.com'
    message = 'added a new file'
    #repo.commit(name=name, email=email, message=message)
    #repo.commit()

    print '\n'.join(list(repo.tracked_files))
    #print repo.modified_files


def main():
    test_new_geounit()

if __name__ == "__main__":
    main()
