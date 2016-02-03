from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore,Security
from flask_login import LoginManager
from flask_restful import Api
#from flask.ext.redis import FlaskRedis

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
app.config.from_object('config')
login_manager.init_app(app)
login_manager.session_protection = "strong"
db = SQLAlchemy(app)
#redis_store = FlaskRedis(app)

from app import model

user_datastore = SQLAlchemyUserDatastore(db,model.User,model.Role)
security = Security(app = app, datastore = user_datastore,register_blueprint = False)

from app import auth