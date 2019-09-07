# -*- coding: utf-8 -*-
"""Test module for user registration and login"""
from flask import current_app
from BenderChess.models import User
from test import app, db, client, session  # noqa: F401
from test.helpers import register_user, create_user, login_user, logout_user


def test_register(session, client):  # noqa: F811
    rv = register_user(client, bad_pw=True)
    assert b'must be equal to password' in rv.data
    user = User.query.filter_by(username=current_app.config['TEST_USER']) \
                     .first()
    assert not user

    rv = register_user(client)
    assert b'you are now a registered user' in rv.data
    user = User.query.filter_by(username=current_app.config['TEST_USER']) \
                     .first()
    assert user in session


def test_login(session, client):  # noqa: F811
    user = create_user(session)
    assert user in session

    rv = login_user(client)
    assert b'Profile' in rv.data

    rv = logout_user(client)
    assert b'Login' in rv.data

    rv = login_user(client, username='badusername')
    assert b'Invalid username or password' in rv.data

    rv = login_user(client, password='badpassword')
    assert b'Invalid username or password' in rv.data


def test_404(session, client):  # noqa: F811
    rv = client.post('/badpath')
    assert b'File Not Found' in rv.data
