from flask import Blueprint
from flask_restplus import Api

auth = Blueprint('auth', __name__)
api = Api(auth)

from . import views