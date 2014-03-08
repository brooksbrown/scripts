#!/usr/bin/env python

# usage: ubuntu-lamp.sh [-h] [--root-mysql-pass ROOT_MYSQL_PASS]
#                       [--apache-mods APACHE_MODS] [--php-version PHP_VERSION]
#                       [--php-timezone PHP_TIMEZONE]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   --root-mysql-pass ROOT_MYSQL_PASS
#                         root mysql password (default: 'pass')
#   --apache-mods APACHE_MODS
#                         comma delimited list of apache modules to enable
#                         (default: rewrite)
#   --php-version PHP_VERSION
#                         version of php to install (options: distributed
#                         [default], latest, previous)
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
	"--php-version",
	help="version of php to install (options: distributed [default], latest, previous)",
	default="distributed"
)

parser.add_argument(
	"--php-timezone",
	help="php timezone (default: MERICA!)",
	default="America/New_York"
)

args = parser.parse_args()

os.system("sudo apt-get update")
os.system("sudo apt-get install -y vim curl wget build-essential python-software-properties")


##php
if args.php_version == "previous":
	os.system("sudo add-apt-repository -y ppa:ondrej/php5-oldstable")
elif args.php_version == "latest":
	os.system("sudo add-apt-repository -y ppa:ondrej/php5")

os.system("sudo apt-get update")
os.system("sudo apt-get install -y php5-cli php5-fpm php5-curl php5-gd php5-xdebug")

#set php timezone
tz_sed_pattern = "s@;date.timezone =.*@date.timezone = " + args.php_timezone +  "@"
os.system("sudo sed -i \"" + tz_sed_pattern + "\" /etc/php5/fpm/php.ini")
os.system("sudo sed -i \"" + tz_sed_pattern + "\" /etc/php5/cli/php.ini")

if args.php_version == "distributed":
	os.system("sudo sed -i \"s/listen = .*/listen = \/var\/run\/php5-fpm.sock/\" /etc/php5/fpm/pool.d/www.conf")

#apache
if args.php_version != "distributed":
	os.system("sudo add-apt-repository -y ppa:ondrej/apache2")
os.system("sudo apt-get update")
os.system("sudo apt-get install -y apache2-mpm-event libapache2-mod-fastcgi")
for mod in args.apache_mods.split(","):
	os.system("sudo a2enmod " + mod)

os.system("sudo apt-get install -y libapache2-mod-php5")


#mysql
os.system("sudo echo \"mysql-server mysql-server/root_password password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo echo \"mysql-server mysql-server/root_password_again password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo apt-get install -y mysql-server")
os.system("sudo apt-get install -y php5-mysql")

os.system("sudo service php5-fpm restart")
os.system("sudo service apache2 restart")
