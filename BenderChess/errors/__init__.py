from flask import Blueprint

bp = Blueprint('errors', __name__)

from BenderChess.errors import routes  # noqa: F401
