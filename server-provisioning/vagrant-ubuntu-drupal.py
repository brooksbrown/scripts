#!/usr/bin/env python

#
# usage: vagrant-ubuntu-drupal.sh [-h] [-dom SITE_DOMAIN]
#                                drupal_docroot database_name database_user
#                                database_pass
#
# positional arguments:
#   drupal_docroot
#   database_name
#   database_user
#   database_pass
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -dom SITE_DOMAIN, --site-domain SITE_DOMAIN
#                        drupal site domain. this is used as the name 
#   --skip-drupal-site-dir
#                        flag to skip the creation and symlinking of a drupal
#                        site directory

import os
import argparse

#arg parsing
parser = argparse.ArgumentParser()
parser.add_argument("drupal_docroot")
parser.add_argument("database_name")
parser.add_argument("database_user")
parser.add_argument("database_pass")

parser.add_argument(
	"--site-domain",
	help="drupal site domain. this is used as the name of the local sites directory (default: localhost)",
	default="localhost",
)

parser.add_argument("--skip-drupal-site-dir", action="store_true", help="flag to skip the creation and symlinking of a drupal site directory")

args = parser.parse_args()

#drush
os.system("sudo apt-get update")
os.system("sudo apt-get -y install php-pear")
os.system("sudo pear channel-discover pear.drush.org")
os.system("sudo pear install drush/drush")

drush_alias_file = ("<?php \n"
					"\$aliases['vagrant'] = array(\n"
					"  'root' => '" + args.drupal_docroot + "',\n"
					"  'uri' => '" + args.site_domain + "',\n"
					"  'db-url' => 'mysql://" + args.database_user + ":" + args.database_pass + "@localhost/" + args.database_name + "',\n"
					");\n")

os.system("mkdir /home/vagrant/.drush")
os.system("echo \"" + drush_alias_file + "\" | tee -a /home/vagrant/.drush/aliases.drushrc.php")
os.system("sudo chown -R vagrant:vagrant /home/vagrant/.drush")
os.system("sudo drush -y dl registry_rebuild --destination=\"/home/vagrant/.drush\"")

#setup a drupal sites directory in the vagrant home directory and symlink into sites directory
if not args.skip_drupal_site_dir:
	local_site_dir_name = "drupal-localhost"
	local_site_dir = "/home/vagrant/" + local_site_dir_name

	os.system("mkdir " + local_site_dir)
	os.system("cp " + args.drupal_docroot + "/sites/default/default.settings.php " + local_site_dir + "/settings.php")
	os.system("sed -i \"s|\$databases = array();|#\$databases = array();|\" " + local_site_dir + "/settings.php")
	drupal_db_settings = ("\$databases['default']['default'] = array(\n"
						  "'driver' => 'mysql',\n"
						  "'database' => '" + args.database_name + "',\n"
						  "'username' => '" + args.database_user + "',\n"
						  "'password' => '" + args.database_pass + "',\n"
						  "'host' => 'localhost',\n"
						  "'prefix' => '',\n"
						  ");")
	os.system("echo \"" + drupal_db_settings + "\" >> " + local_site_dir + "/settings.php")

	os.system("mkdir " + local_site_dir + "/files")
	os.system("chown -R www-data:www-data " + local_site_dir + "/files")

	os.system("ln -s " + local_site_dir + " " + args.drupal_docroot + "/sites/" + args.site_domain)

#create the db
os.system("mysql -u " + args.database_user + " -p" + args.database_pass + " -e \"create database " + args.database_name + ";\"")

