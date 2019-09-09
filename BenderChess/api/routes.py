from flask import jsonify
# from BenderChess import db
from BenderChess.api import bp


@bp.route('/hello')
def api_hello():
    return jsonify("let's play chess")
