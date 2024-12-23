from flask import Blueprint

bp = Blueprint("account", __name__)

from app.account_core import routes
