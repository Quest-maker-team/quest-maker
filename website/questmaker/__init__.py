"""questmaker

This module contains questmaker application that can be run from terminal using `flask run` command.
This file can also be imported as a module and contains the following
functions:

    * create_app - create and configure the questmaker app that can be run from python code
"""

from flask import Flask, render_template
from flask_login import current_user
from flask_manage_webpack import FlaskManageWebpack

def create_app(test_config=None):
    """Create and configure the questmaker app
    :param test_config: defines test or prod configuration
    :return: configured app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)

    from . import db
    db.init_app(app)

    from .auth import auth, login_manager
    app.register_blueprint(auth)
    login_manager.init_app(app)

    from .profile import prof
    app.register_blueprint(prof)

    manage_webpack = FlaskManageWebpack()
    manage_webpack.init_app(app)

    @app.route('/')
    def index():
        """
        Main questmaker page
        :return: main questmaker page
        """
        return render_template('index.html', user=current_user)

    @app.route('/constructor.html')
    def constructor():
        """
        Constructor page
        :return: constructor page
        """
        return render_template('constructor.html', user=current_user)

    return app
