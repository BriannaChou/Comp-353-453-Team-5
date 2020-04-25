#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"
# Default sql file is create_db_complex, else use the provided value
if [[ -z ${1} || ! -f ${1} ]];then
	SQL_PATH="./sql/create_db.sql"
else
	SQL_PATH="${1}"
fi

mysql -u'CS353_ChatApp' -p'Jpjb!2020' -h 52.87.177.126 < $SQL_PATH 
