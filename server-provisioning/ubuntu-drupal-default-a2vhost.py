#!/usr/bin/env python

# usage: ubuntu-drupal-default-a2vhost.sh [-h] [-d DOCROOT]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -d DOCROOT, --docroot DOCROOT

import os
import sys
import argparse

#arg parsing
parser = argparse.ArgumentParser()

parser.add_argument(
	"-d",
	"--docroot",
	default="/var/www",
)

args = parser.parse_args()

vhost_file = ("<VirtualHost *:80>\n"
			  " DocumentRoot " + args.docroot + "\n"
			  " <Directory \"" + args.docroot + "\">\n"
			  "  Options Includes FollowSymLinks\n"
			  "  AllowOverride All\n"
			  "  Order allow,deny\n"
			  "  Allow from all\n"
			  " </Directory>\n"
			  "</VirtualHost>\n")


#detect default vhost
if os.path.isfile("/etc/apache2/sites-available/default"):
	default_vhost_file = "/etc/apache2/sites-available/default"
elif os.path.isfile("/etc/apache2/sites-available/000-default.conf"):
	default_vhost_file = "/etc/apache2/sites-available/000-default.conf"
else:
	os.system("echo \"default virtual host file not detected\"")
	sys.exit(0)

os.system("sudo rm -r " + default_vhost_file)
os.system("sudo touch " + default_vhost_file)
os.system("echo \"" + vhost_file + "\" | sudo tee -a " + default_vhost_file)

os.system("sudo service apache2 restart")
