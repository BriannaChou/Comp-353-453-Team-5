#!/bin/bash
if [ ! -f chat_app/sql_config.py ]; then
	./exec_sql.sh
fi
export FLASK_APP=chat_app/app.py
export FLASK_DEBUG=1
flask run
