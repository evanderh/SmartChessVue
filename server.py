from app import create_app, db
from app.models import User, Game


app = create_app()


@app.shell_context_processor
def make_shell():
    return {'db': db,
            'User': User,
            'Game': Game}
