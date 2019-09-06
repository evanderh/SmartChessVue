from flask import Blueprint

bp = Blueprint('main', __name__)

from BenderChess.main import routes
