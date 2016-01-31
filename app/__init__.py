from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
app.config.from_object('config')
login_manager.init_app(app)
login_manager.session_protection = "strong"
db = SQLAlchemy(app)

from app import user, model
