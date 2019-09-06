from flask import Flask

def create_app():
    """App factory for BenderChess"""
    app = Flask(__name__)

    from BenderChess.main import bp as mainbp
    app.register_blueprint(mainbp)

    return app

