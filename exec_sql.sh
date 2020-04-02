#!/bin/bash

SQL_PATH=$1
cd "$(dirname "${BASH_SOURCE[0]}")"
# Default sql file is create_db_complex, else use the provided value
[ ! $SQL_PATH ] && SQL_PATH=sql/create_db_complex.sql

if [ ! -f flask_app/sql_config.py ]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username=\"$username\";password=\"$password\"" > flask_app/sql_config.py
	chmod 600 flask_app/sql_config.py
fi

source flask_app/sql_config.py
mysql -u"$username" -p"$password" < $SQL_PATH 
