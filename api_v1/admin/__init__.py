from flask import Blueprint
from flask_restplus import Api

admin = Blueprint('admin', __name__)
api = Api(admin)

from . import views
