import pytest

from app import create_app
from app import db as _db
from test.helpers import create_user
import config


@pytest.fixture(scope='session')
def app(request):
    # Set up
    app = create_app(config.TestConfig)
    ctx = app.app_context()
    ctx.push()
    yield app
    # Teardown
    ctx.pop()


@pytest.fixture(scope='session')
def db(app, request):
    # Set up
    _db.create_all()
    yield _db
    # Teardown
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(scope='session')
def client(app, request):
    yield app.test_client()


@pytest.fixture(scope='function')
def session(db, request):
    # Set up
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session
    yield session
    # Teardown
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='function')
def user(session):
    user = create_user(session)
    yield user
