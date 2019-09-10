from flask import jsonify
# from BenderChess import db
from BenderChess.api import bp


@bp.route('/timeControls')
def timeControls():
    return jsonify(["1+0", "3+0", "5+0"])
