#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"
# Default sql file is create_db_complex, else use the provided value
if [[ -z ${1} || ! -f ${1} ]];then
	SQL_PATH="./sql/create_db.sql"
else
	SQL_PATH="${1}"
fi

if [ ! -f chat_app/sql_config.py ]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username=\"$username\";password=\"$password\"" > chat_app/sql_config.py
	chmod 600 chat_app/sql_config.py
fi

source chat_app/sql_config.py
mysql -u"$username" -p"$password" < $SQL_PATH 
[ $? -eq 1 ] && rm chat_app/sql_config.py
