#!/bin/bash

[ ! $1 ] && >&2 echo "Please provide a .sql file as a parameter" && exit 1

# In case if this script is being executed from some different directory, 
# take note of the absolute path of the provided SQL file then cd into 
# the directory in which this script is held
SQL_PATH="$(pwd)/$1"
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -f flask_app/.mysql.cfg ]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username=\"$username\";password=\"$password\"" > flask_app/.mysql.cfg
	chmod 600 flask_app/.mysql.cfg
fi

source flask_app/.mysql.cfg
mysql -u"$username" -p"$password" < $SQL_PATH 
