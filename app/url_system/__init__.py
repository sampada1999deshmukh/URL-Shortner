from flask import Blueprint

bp = Blueprint("URL", __name__)

from . import routes, service