scids-client is a python library for accessing provenance data and interacting with GeoDataspace server. 

Pre-requirements:
* git   
* python dev 
* g++
* docker
* dulwich
* levelDB
* sudo apt-get install python-setuptools

sudo chmod o+rwx /var/run/docker.sock

git clone https://<username>@github.com/sumanth1105/scids-client.git

Install:
Use the setup.py script to install this library:

cd scids-client
sudo python setup.py install

The library can also be installed as a normal user in a virtualenv, or using the --user option to install.


Usage:
This is a stand alone git like offline client which can be connected to geodataspace server.
The client requires a goauth token to authenticate.

Edit config parameters in the ~/.gdsclient/config.ini file


Known Errors:
error: Setup script exited with error in docker-py setup command: Invalid environment marker: python_version < "3.5"
Run: pip install setuptools --upgrade