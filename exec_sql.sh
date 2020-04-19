#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"
# Default sql file is create_db_complex, else use the provided value
if [[ -z ${1} || ! -f ${1} ]];then
	SQL_PATH="./sql/create_db_complex.sql"
else
	SQL_PATH="${1}"
fi

if [ ! -f flask_app/sql_config.py ]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username=\"$username\";password=\"$password\"" > flask_app/sql_config.py
	chmod 600 flask_app/sql_config.py
fi

source flask_app/sql_config.py
mysql -u"$username" -p"$password" < $SQL_PATH 
[ $? -eq 1 ] && rm flask_app/sql_config.py
