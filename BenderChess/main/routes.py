import os
import jwt
from datetime import datetime, timedelta
from flask import (
    send_file, request, current_app, jsonify
)
from BenderChess import db
from BenderChess.main import bp
from BenderChess.models import User


@bp.before_app_request
def before_request():
    current_app.logger.debug('Incoming request')
    # if current_user.is_authenticated:
    #     current_user.last_seen = datetime.utcnow()
    #     db.session.commit()


@bp.route('/')
def home():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({
            'message': 'Invalid credentials',
            'authenticated': False
        }), 401

    payload = {'sub': user.username,
               'iat': datetime.utcnow(),
               'exp': datetime.utcnow() - timedelta(hours=1)}

    token = jwt.encode(payload,
                       current_app.config['SECRET_KEY'],
                       algorithm='HS256')

    return jsonify({'token': token.decode('UTF-8')})

# @bp.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('main.home'))


@bp.route('/register', methods=['POST'])
def register():
    """Account sign up"""
    data = request.get_json()

    # TODO: Validate user before creation
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201
