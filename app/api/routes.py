from flask import jsonify
# from app import db
from app.api import bp

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


@bp.route('/game', methods=['GET'])
def game_api_get():
    # Get all games
    return jsonify(games)


@bp.route('/game', methods=['POST'])
def game_api_post():
    # Create a new game and return its' id
    # For now always return an id of 2
    # TODO: Create a new game
    return jsonify(2)


@bp.route('/game/<string:id>')
def getGameID(id):
    return jsonify(games[id])
