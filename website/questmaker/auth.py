"""
Contains functions for signup, login and logout functionality
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import LoginForm, SignupFrom
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .UserLogin import AuthorLogin
from . import db

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Необходима авторизация'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(author_id):
    """
    Callback function for flask-login
    :param author_id: user id
    :return: object of UserLogin class inited with data from db
    """
    author = db.get_author_by_id(author_id)
    return AuthorLogin(author) if author else None


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Contains signup functionality
    :return: signup page or redirect to login
    """
    form = SignupFrom()  # WT from
    if form.validate_on_submit():  # check if all field are correct
        name = form.name.data
        email = form.email.data
        psw = form.psw.data
        hash_psw = generate_password_hash(psw)
        success = db.add_user(name, hash_psw, email)
        if success:
            flash('Вы зарегестрированы', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Вы уже зарегестрированы', 'error')
    return render_template('signup.html', title='Регистрация | QM', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """
    Contains login functionality
    :return: login page or redirect to next page that required login
    """
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = LoginForm()  # WT form
    if form.validate_on_submit():  # check if all field are correct
        email = form.email.data
        psw = form.psw.data
        author = db.get_author_by_email(email)
        if author:
            if check_password_hash(author['password'], psw):
                print(form.remember.data)
                login_user(AuthorLogin(author), form.remember.data)

                return redirect(request.args.get('next') or url_for('profile.profile'))
            else:
                flash('Неверный пароль', 'error')
        else:
            flash('Пользователь с таким email не зарагастрирован', 'error')
    return render_template('login.html', title='Вход | QM', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Contains logout functionality
    :return: redirect user to login page
    """
    logout_user()
    return redirect(url_for('auth.login'))
