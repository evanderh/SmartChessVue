import os
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

import config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_obj=config.Config):
    """App factory for Bender Chess"""

    # Create + configure app
    app = Flask(__name__, static_folder='../dist/static')
    app.config.from_object(config_obj)

    # Init plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'

    # TODO: Enable CORS only on domain of front end app
    CORS(app)

    # Add blueprints
    from app.errors import bp as errorsbp
    app.register_blueprint(errorsbp)
    from app.main import bp as mainbp
    app.register_blueprint(mainbp)
    from app.api import bp as apibp
    app.register_blueprint(apibp, url_prefix='/api')

    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.config.dictConfig(app.config['LOGCONFIG'])

    return app


from app import models  # noqa: E403, F401
