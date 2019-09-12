import uuid
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from BenderChess import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False,
                     default=uuid.uuid4)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Basic user info
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    username = db.Column(db.String(128), index=True, unique=True,
                         nullable=False)

    # Metadata
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    games = db.relationship("Game",
                            primaryjoin="or_(User.id==Game.white_id, "
                                        "User.id==Game.black_id)")

    def __init__(self, raw_password, **kwargs):
        super().__init__(**kwargs)
        self.set_password(raw_password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User username={self.username}>"


class Game(db.Model):
    __tablename__ = "games"

    # Identification
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False,
                     default=uuid.uuid4().hex)

    # Game data
    fen = db.Column(db.String(128), nullable=False)
    white_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    black_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    white_player = db.relationship("User", foreign_keys=[white_id])
    black_player = db.relationship("User", foreign_keys=[black_id])

    def __repr__(self):
        return f"<Game fen={self.fen}>"


@login.user_loader
def load_user(id):
    """Flask-login user loader"""
    return User.query.get(int(id))
