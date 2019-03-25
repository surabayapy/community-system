# third-party imports
from flask import Flask
from flask_restplus import Api, Resource
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://surabayapy:pythonsby@surabayapy.mysql.pythonanywhere-services.com/surabayapy$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app=app)
db = SQLAlchemy(app)
login_manager = LoginManager()

import api_v1.models

login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

from .admin import admin as admin_bp
from .home import home as home_bp
from .auth import auth as auth_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)