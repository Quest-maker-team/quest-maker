from flask import Blueprint, request, render_template, flash, redirect
from .forms import LoginForm, SignupFrom
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupFrom()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        psw = form.psw.data
        if True:
            flash('Вы зарегестрированы', 'success')
            return redirect('login')
        else:
            flash('Ошибка', 'error')
    return render_template('signup.html', title='Регистрация | QM', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if False: # if current_user.authorized -> redirect to profile
        pass
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        psw = form.psw.data
        # check password
        flash('Неверный пароль', 'error')
    return render_template('login.html', title='Вход | QM', form=form)


@auth.route('/logout')
def logout():
    return 'logout'
