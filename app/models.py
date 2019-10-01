import jwt
import uuid
from flask import current_app, g, jsonify
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False,
                     default=uuid.uuid4)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True,
                      nullable=False)
    username = db.Column(db.String(128), index=True, unique=True,
                         nullable=False)

    # Metadata
    admin = db.Column(db.Boolean, default=False, nullable=False)
    bot = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    games = db.relationship("Game", back_populates="player", lazy='dynamic')

    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        # Validate request
        if not username or not password:
            return None

        # Check user + password
        user = cls.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return None

        return user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return dict(id=self.id,
                    uuid=self.uuid,
                    username=self.username)

    def __repr__(self):
        return f"<User username={self.username}>"


DEFAULT_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR  w KQkq - 0 1'
DEFAULT_HISTORY = {
    'moves': [],
}


class Game(db.Model):
    __tablename__ = "games"

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False,
                     default=uuid.uuid4)

    # Essential game data
    result = db.Column(db.String(8), nullable=False, default='*')
    ply_count = db.Column(db.Integer, default=0)
    time_control_field = db.Column(db.String(128), default='-')
    termination = db.Column(db.String(128), default='unterminated')
    startfen = db.Column(db.String(128), nullable=False, default=DEFAULT_FEN)
    history = db.Column(db.JSON, nullable=False, default=DEFAULT_HISTORY)
    mode = db.Column(db.String(128), nullable=False, default='analysis')

    # Relationship with user
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    player = db.relationship("User", back_populates="games")

    def to_dict(self):
        return dict(id=self.id,
                    uuid=self.uuid,
                    result=self.result,
                    ply_count=self.ply_count,
                    time_control_field=self.time_control_field,
                    termination=self.termination,
                    startfen=self.startfen,
                    history=self.history,
                    mode=self.mode)

    def __repr__(self):
        return f"<Game fen={self.fen}>"


unauthorized_header = {
    'message': 'Invalid token. Authentication required',
    'authenticated': False
}
expired_header = {
    'message': 'Expired token. Reauthentication required.',
    'authenticated': False
}

# Configure flask-login request loader
@login.request_loader
def load_user_from_request(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        g.unauthorized_header = unauthorized_header
        return None

    try:
        token = auth_headers[1]
        data = jwt.decode(token,
                          current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
        user = User.query.filter_by(email=data['sub']).first()
        if user:
            return user
    except jwt.ExpiredSignatureError as e:
        current_app.logger.debug(e)
        g.unauthorized_response = unauthorized_header
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.debug(e)
        g.unauthorized_response = expired_header
        return None

    return None


@login.unauthorized_handler
def unauthorized():
    if 'unauthorized_response' in g:
        return jsonify(g.unauthorized_response), 401
    else:
        return jsonify(unauthorized_header), 401
