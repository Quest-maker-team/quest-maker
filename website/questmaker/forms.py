"""
Contains WTForms that are used by application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """
    Login WTForm with some validators
    """
    email = EmailField('Email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    psw = PasswordField('Пароль', validators=[DataRequired()], render_kw={'placeholder': 'Пароль'})
    remember = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class SignupFrom(FlaskForm):
    """
    Signup WTForm with some validators
    """
    name = StringField('Имя', validators=[DataRequired()], render_kw={'placeholder': 'Имя'})
    email = EmailField('Email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})

    psw = PasswordField('Пароль',
                        validators=[DataRequired()], render_kw={'placeholder': 'Пароль'})

    psw_confirm = PasswordField('Подтверждение пароля',
                                validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')],
                                render_kw={'placeholder': 'Повторите пароль'})

    submit = SubmitField('Зарегестрироваться')