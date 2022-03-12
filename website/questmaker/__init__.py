"""questmaker

This module contains questmaker application that can be run from terminal using `flask run` command.
This file can also be imported as a module and contains the following
functions:

    * create_app - create and configure the questmaker app that can be run from python code
"""

from flask import Flask, render_template


def create_app(test_config=None):
    """Create and configure the questmaker app
    :param test_config: defines test or prod configuration
    :return: configured app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)

    from . import db
    db.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
