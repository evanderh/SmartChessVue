from datetime import datetime
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from BenderChess import db
from BenderChess.main import bp
from BenderChess.models import User
from BenderChess.main.forms import LoginForm, RegistrationForm


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def home():
    return render_template('index.html', title='Home')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in, if so, send to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Get the user for the login attempt
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not user.check_password(form.password.data):
            # If invalid login, let the user retry
            flash("Invalid username or password.")
            return redirect(url_for('main.login'))

        # Login and redirect the user to the next page
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)

    # Otherwise, render the login page
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Account sign up"""
    # Check if user is already logged in, if so, send to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Create the user and add them to the database
        user = User(username=form.username.data, email=form.email.data,
                    raw_password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Redirect to login
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))

    # Otherwise, render the registration page
    return render_template('register.html', title='Register', form=form)
