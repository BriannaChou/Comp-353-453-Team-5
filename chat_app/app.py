import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sql_config import username, password

# Flask and SQL setup 
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Either set the connection string as an environment variable or set credentials in the sql_config.py file
# Example:
#   Environment Variable Name: SQLALCHEMY_DATABASE_URI
#   Environment Variable Value: mysql+mysqlconnector://YourName:YourPassword@localhost/ChatApp
connectionString = os.environ.get('SQLALCHEMY_DATABASE_URI')
if connectionString:
    app.config['SQLALCHEMY_DATABASE_URI'] = connectionString
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + username + ':' + password + '@localhost/ChatApp'

db = SQLAlchemy(app)
login_manager = LoginManager()
bcrypt = Bcrypt()

# Initialize plugins
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Logging setup 
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

import models
models.db.create_all()

import routes

if __name__ == '__main__':
    app.run(debug=True)

db.engine.execute("INSERT IGNORE INTO Department VALUES ('Customer Service');")
db.engine.execute("INSERT IGNORE INTO Department VALUES ('Tech Support');")
