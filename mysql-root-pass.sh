#!/usr/bin/env bash

service mysql stop
mysqld --skip-grant-tables &
sleep 2
mysql -u root mysql -e "update user set password=PASSWORD(\"$1\") where User='root';"
mysql -u root mysql -e "flush privileges;"
killall mysqld
service mysql start
history -d 6
