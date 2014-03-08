#!/usr/bin/env python

# usage: ubuntu-lamp.sh [-h] [-mods APACHE_MODS] [-phpv PHP_VERSION]
#                       [-phptz PHP_TIMEZONE]
#                       root_mysql_passwd
# 
# positional arguments:
#   root_mysql_passwd
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -mods APACHE_MODS, --apache-mods APACHE_MODS
#                         comma delimited list of apache modules to enable
#                         (default: rewrite)
#   -phpv PHP_VERSION, --php-version PHP_VERSION
#                         version of php to install (options: distributed
#                         [default], latest, previous)
#   -phptz PHP_TIMEZONE, --php-timezone PHP_TIMEZONE
#                         php timezone (default: MERICA!)
# 

import os
import argparse

#arg parsing
parser = argparse.ArgumentParser()

parser.add_argument(
	"-mods",
	"--apache-mods",
	help="comma delimited list of apache modules to enable (default: rewrite)",
	default="rewrite"
)

parser.add_argument(
	"-phpv",
	"--php-version",
	help="version of php to install (options: distributed [default], latest, previous)",
	default="distributed"
)

parser.add_argument(
	"-phptz",
	"--php-timezone",
	help="php timezone (default: MERICA!)",
	default="America/New_York"
)

parser.add_argument("root_mysql_passwd")

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
os.system("sudo add-apt-repository -y ppa:ondrej/apache2")
os.system("sudo apt-get update")
os.system("sudo apt-get install -y apache2-mpm-event libapache2-mod-fastcgi")
for mod in args.apache_mods.split(","):
	os.system("sudo a2enmod " + mod)

os.system("sudo apt-get install -y libapache2-mod-php5")


#mysql
os.system("sudo echo \"mysql-server mysql-server/root_password password " + args.root_mysql_passwd + "\" | debconf-set-selections")
os.system("sudo echo \"mysql-server mysql-server/root_password_again password " + args.root_mysql_passwd + "\" | debconf-set-selections")
os.system("sudo apt-get install -y mysql-server")
os.system("sudo apt-get install -y php5-mysql")

os.system("sudo service php5-fpm restart")
os.system("sudo service apache2 restart")
