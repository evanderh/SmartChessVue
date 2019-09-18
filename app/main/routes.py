import os
import jwt
import uuid
import time
from datetime import datetime, timedelta
from flask import send_file, request, current_app, jsonify, g
from app import db
from app.main import bp
from app.models import User


@bp.before_app_request
def before_request():
    g.requestID = uuid.uuid4().hex
    current_app.logger.debug('Recieved request')
    g.start = time.time()


@bp.after_app_request
def after_request(response):
    g.status = response.status
    g.status_code = response.status_code
    elapsed = round(time.time() - g.get('start', time.time()), 4)
    current_app.logger.debug(f'Response took {elapsed}s')
    return response


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


@bp.route('/register', methods=['POST'])
def register():
    """Account sign up"""
    data = request.get_json()

    # TODO: Validate user before creation
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201
