#!/usr/bin/env python

#
# usage: vagrant-ubuntu-laravel.sh [-h] 
#

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("docroot")
parser.add_argument("database_name")
parser.add_argument("database_user")
parser.add_argument("database_pass")

args = parser.parse_args()

os.system("sudo apt-get install -y php5-mcrypt")
os.system("sudo service php5-fpm restart")

# create a nginx vhost
vhost = ("server {\n"
         "	listen   80;\n"
         " 	root " + args.docroot + ";\n"
         "	index index.php index.html index.htm;\n"
	 	 "	location / {\n"
         "	     try_files \$uri \$uri/ /index.php\$is_args\$args;\n"
	     "	}\n"
	     "	# pass the PHP scripts to FastCGI server listening on /var/run/php5-fpm.sock\n"
		 "  location ~ \.php\$ {\n"
	     "		fastcgi_split_path_info ^(.+\.php)(/.+)\$;\n"
         "		fastcgi_pass unix:/var/run/php5-fpm.sock;\n"
		 "		fastcgi_index index.php;\n"
		 "		include fastcgi_params;\n"
		 "	}\n"
		 "}\n")

os.system("echo \"" + vhost + "\" | sudo tee -a /etc/nginx/sites-available/vagrant")
os.system("sudo ln -s /etc/nginx/sites-available/vagrant /etc/nginx/sites-enabled/vagrant")
os.system("sudo rm /etc/nginx/sites-enabled/default")
os.system("sudo service nginx restart")

# install composer
os.system("curl -sS https://getcomposer.org/installer | php")
os.system("mv composer.phar /usr/local/bin/composer")

#create the db
os.system("mysql -u " + args.database_user + " -p" + args.database_pass + " -e \"create database " + args.database_name + ";\"")
