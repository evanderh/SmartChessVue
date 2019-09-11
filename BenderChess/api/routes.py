from flask import jsonify
# from BenderChess import db
from BenderChess.api import bp

games = {
    '1': {
        'id': '1',
        'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR  w KQkq - 0 1',
    },
    '2': {
        'id': '2',
        'fen': 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1',
    },
}


@bp.route('/user/<string:username>')
def getUser(username):
    return jsonify({
        'username': username
    })


@bp.route('/game/<string:id>')
def getGame(id):
    return jsonify(games[id])
