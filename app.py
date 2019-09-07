from BenderChess import create_app, db
from BenderChess.models import User


app = create_app()


@app.shell_context_processor
def make_shell():
    return { 'db': db, 
             'User': User }
