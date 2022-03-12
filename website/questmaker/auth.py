from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    return render_template('signup.html', title='Регистрация | QM')


@auth.route('/login')
def login():
    return render_template('login.html', title='Вход | QM')


@auth.route('/logout')
def logout():
    return 'logout'
