#!/bin/bash
[ ! $1 ] && >&2 echo "Please provide a .sql file as a parameter" && exit 1
if [ ! -f .mysql.cfg ]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username=\"$username\";password=\"$password\"" > .mysql.cfg
	chmod 600 .mysql.cfg
fi
source .mysql.cfg
mysql -u"$username" -p"$password" < $1 
