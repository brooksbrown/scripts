#!/usr/bin/env python

# usage: ubuntu-saucy-lamp.sh [-h] [--root-mysql-pass ROOT_MYSQL_PASS]
#                       [--apache-mods APACHE_MODS] [--php-version PHP_VERSION]
#                       [--php-timezone PHP_TIMEZONE]
# # optional arguments:
#   -h, --help            show this help message and exit
#   --root-mysql-pass ROOT_MYSQL_PASS
#                         root mysql password (default: 'pass')
#   --apache-mods APACHE_MODS
#                         comma delimited list of apache modules to enable
#                         (default: rewrite)
#   --php-timezone PHP_TIMEZONE
#                         php timezone (default: MERICA!)

import os
import argparse

#arg parsing
parser = argparse.ArgumentParser()

parser.add_argument(
	"--root-mysql-pass",
	help="root mysql password (default: \'pass\')",
	default="pass",
)

parser.add_argument(
	"--apache-mods",
	help="comma delimited list of apache modules to enable (default: rewrite)",
	default="rewrite"
)

parser.add_argument(
	"--php-timezone",
	help="php timezone (default: MURICA!)",
	default="America/New_York"
)

args = parser.parse_args()

os.system("sudo apt-get update")
os.system("sudo apt-get install -y vim curl wget build-essential python-software-properties")

#install php
os.system("sudo apt-get install -y php5 php5-cli php5-curl php5-json php5-gd php5-xdebug")
os.system("sudo sed -i \"s@disable_functions =*@;disable_functions.*@\" /etc/php5/cli/php.ini")

#install apache
os.system("sudo apt-get install apache2")
os.system("sudo apt-get install libapache2-mod-php5")

for mod in args.apache_mods.split(","):
	os.system("sudo a2enmod " + mod)

#install mysql
os.system("sudo echo \"mysql-server mysql-server/root_password password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo echo \"mysql-server mysql-server/root_password_again password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo apt-get install -y mysql-server mysql-client")
os.system("sudo apt-get install -y php5-mysql")

#set php timezone
tz_sed_pattern = "s@;date.timezone =.*@date.timezone = " + args.php_timezone +  "@"
os.system("sudo sed -i \"" + tz_sed_pattern + "\" /etc/php5/apache2/php.ini")
os.system("sudo sed -i \"" + tz_sed_pattern + "\" /etc/php5/cli/php.ini")

os.system("sudo service apache2 restart")
