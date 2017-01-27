#!/usr/bin/python

import os, sys
import configparser

class GDSConfig:
    config_file_name = None
    config = None

    ## Read the config.ini file and check if server URL is set
    ## if serve is not set, ask to set it and exit
    ## if username is none ask for username and store it config.ini.
    ## Next time the client is run, read username from config.ini
    ## If Globus token is none, Obtain Globus token and store it, else proceed
    ## Return config
    def __init__(self):
        self.config_file_name = os.path.join(os.path.expanduser("~"),'.gdsclient','config.ini')
        #print "config file path: %s" %self.config_file_name
        self.config = configparser.ConfigParser()
        try:
            self.config.read_file(open(self.config_file_name))
        except:
            self.config['Client'] = {'client-id': "test-client"}
            self.config['Server'] = {'server-url': "https://ec2-54-84-57-85.compute-1.amazonaws.com/service/dataset",
                                   'server-type' : 'globus'}
            self.config['GeoDataspace'] = {'uname' : 'tanum'}
            self.config['Globus'] = {
                'globus-uname': 'tanum',
                'globus-catalog': 11,
                'globus-local-endpoint': 'tanum#client153',
                'globus-local-endpoint': 'tanum#client153',
                'globus-remote-endpoint': 'tanum#geodataserver',
                'globus-local-folder': '/home/ubuntu/.gdclient/docker_images',
                'globus-remote-folder': '/home/ubuntu/globus/tanum',
                'goauth-token': 'None'
                }
            self.write_cfg_file()

    def write_cfg_file(self):
        with open(self.config_file_name, 'w') as configfile:
            self.config.write(configfile)

    def get_cfg_field(self, field, namespace='Default'):
        try:
            return str(self.config.get(namespace, field))
        except:
            print "%s is not defined"% field
            return "None"

'''
    def init_globus_catalog(self, datasetClient=None):
        if self.get_cfg_field('server-type', 'Server') != "globus":
            print "GeoDataspace Server is not set to be Globus in %s"%self.config_file_name
            exit(1)

        if self.get_cfg_field('server-url', 'Server') == "None":
            print "GeoDataspace Server URL is not set in %s"%self.config_file_name
            exit(1)

        b_will_exit = False
        if  self.get_cfg_field('uname', 'Globus') == "None":
            uname = raw_input("Please provide user name > ")
        else:
            uname = self.get_cfg_field('uname')

        if self.get_cfg_field('goauth-token', 'Globus') == "None":
            b_will_exit = True
            try:
                result = get_access_token(username=uname)
                self.config['Globus']['uname']=uname
                self.config['Globus']['goauth-token']= result.token
                b_will_exit = False
            except Exception as e:
                print "There was an error in obtaining Globus token. Please check username or your password"
                sys.stderr.write(str(e) + "\n")

        catalog_id = self.get_cfg_field('catalog',namespace='GeoDataspace')
        if  catalog_id == "None":
            nr_tries = 0
            while (nr_tries<3 and catalog_id == "None"):
                catalog_name = raw_input("Please provide catalog name > ")
                # Show the data to user and get catalog_name from user
                catalog_json = get_catalog_by_name(datasetClient,catalog_name)
                if catalog_json is not None:
                    catalog_id = str(catalog_json.get('id',None))
                    self.config['GeoDataspace']['catalog'] = catalog_id
                else:
                    print "Could not find catalog with name containing '%s'"%catalog_name
                nr_tries += 1

            self.write_cfg_file()
                if b_will_exit:
            print "Thank you for setup. Please run client again"
            exit(1)

        self.write_cfg_file()
        return catalog_id
'''

'''
if __name__ == "__main__":
    config = GDSConfig();
'''
