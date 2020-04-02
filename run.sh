#!/bin/bash
if [ ! -f flask_app/sql_config.py ]; then
	./exec_sql.sh
fi
export FLASK_APP=flask_app/app.py
export FLASK_DEBUG=1
flask run
