# -*- coding: utf-8 -*-
"""Helper functions for test modules"""
from flask import current_app

from app.models import User


def login_user(client, username=None, password=None):
    username = current_app.config['TEST_USER'] if not username else username
    password = current_app.config['TEST_PASS'] if not password else password

    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)


def logout_user(client):
    return client.get('/logout', follow_redirects=True)


def register_user(client, username=None, password=None, bad_pw=False):
    username = current_app.config['TEST_USER'] if not username else username
    password = current_app.config['TEST_PASS'] if not password else password
    password2 = password if not bad_pw else f"x_{password}"

    return client.post('/register', data={
        'username': username,
        'password': password,
        'password2': password2,
        'email': f"{username}@example.com"
    }, follow_redirects=True)


def create_user(session, username=None, password=None):  # noqa: F811
    username = current_app.config['TEST_USER'] if not username else username
    password = current_app.config['TEST_PASS'] if not password else password

    user = User(username=username,
                email=f"{username}@example.com",
                raw_password=password)
    session.add(user)
    session.commit()
    return user
