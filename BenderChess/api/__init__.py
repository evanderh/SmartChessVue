from flask import Blueprint

bp = Blueprint('api', __name__)

from BenderChess.api import routes  # noqa: F401
