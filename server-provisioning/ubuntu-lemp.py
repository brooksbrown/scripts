#!/usr/bin/env python

# usage: ubuntu-raring-lemp.sh [-h] [--root-mysql-pass ROOT_MYSQL_PASS]
#                       [--php-version PHP_VERSION]
#                       [--php-timezone PHP_TIMEZONE]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   --root-mysql-pass ROOT_MYSQL_PASS
#                         root mysql password (default: 'pass')
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

#nginx
os.system("sudo add-apt-repository -y ppa:nginx/stable")
os.system("sudo apt-get update")
os.system("sudo apt-get -y install nginx")

os.system("sudo sed -i \"s/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/\" /etc/php5/fpm/php.ini")


#mysql
os.system("sudo echo \"mysql-server mysql-server/root_password password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo echo \"mysql-server mysql-server/root_password_again password " + args.root_mysql_pass + "\" | debconf-set-selections")
os.system("sudo apt-get install -y mysql-server")
os.system("sudo apt-get install -y php5-mysql")

os.system("sudo service php5-fpm restart")
os.system("sudo service nginx restart")
