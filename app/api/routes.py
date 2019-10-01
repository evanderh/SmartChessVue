from flask import jsonify, current_app
from flask_login import current_user
from app import db
from app.api import bp
from app.models import Game


@bp.route('/games', methods=['GET'])
def game_api_get():
    current_app.logger.debug('getting all games')

    games = Game.query.all()
    return jsonify([game.to_dict() for game in games])


@bp.route('/games', methods=['POST'])
def game_api_post():
    current_app.logger.debug(f'creating game')

    if current_user.is_anonymous:
        game = Game()
    else:
        game = Game(player=current_user)

    db.session.add(game)
    db.session.commit()

    return jsonify(game.to_dict())


@bp.route('/games/<int:id>')
def game_api_get_game(id):
    user = current_user
    current_app.logger.debug(f'getting game {id} for {user}')

    game = Game.query.get(id)
    return jsonify(game.to_dict())
