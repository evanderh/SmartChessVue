from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_obj=config.Config):
    """App factory for Bender Chess"""

    # Create + configure app
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Init plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'

    # Add blueprint
    from BenderChess.main import bp as mainbp
    app.register_blueprint(mainbp)

    return app


from BenderChess import models  # noqa: E402, F401
