#!/usr/bin/python

import os, sys, re
from geodataspace.client.datastore.geodatamanager import GeoDataManager
from geodataspace.client.datastore.geounit import GeoUnit

def test_geodatamanager():
    gdclient_dir = '/tmp/gdsclient/'
    geodatamanger = GeoDataManager(gdclient_dir)
    geounit_name = 'test'

    g = GeoUnit(geounit_name, geodatamanger)
    geodatamanger.delete_geounit(geounit_name)
    g.delete()

def main():
    test_geodatamanager()

if __name__ == "__main__":
    main()
