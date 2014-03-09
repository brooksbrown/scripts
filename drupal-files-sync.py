#!/usr/bin/env python

# usage: drupal-files-sync.sh [-h] [-d DOCROOT] [-e ENVIRONMENT]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -d DOCROOT, --docroot DOCROOT
#   -e ENVIRONMENT, --environment ENVIRONMENT

import os
import sys
import argparse

remote_files = {
	"dev" : {
		"user" : "",
		"host" : "",
		"files_location" : "",
	}
}
destination = ""

#arg parsing
parser = argparse.ArgumentParser()

parser.add_argument(
	"-d",
	"--docroot",
	default="/var/www",
)

parser.add_argument(
	"-e",
	"--environment",
	default="",
)
args = parser.parse_args()

env_keys = list(remote_files.keys())

if args.environment != "" and args.environment not in env_keys:
	os.system("environment not available")
	sys.exit(0)

if args.environment == "":
	args.environment = remote_files[env_keys[0]]

os.system("rsync -ave 'ssh' " + args.environment['user'] + "@" + args.environment['host'] + ":" + args.environment['files_location'] + " " + destination)

