"""questmaker

This module contains questmaker application that can be run from terminal using `flask run` command.
This file can also be imported as a module and contains the following
functions:

    * create_app - create and configure the questmaker app that can be run from python code
"""

import os

from flask import Flask, render_template


def create_app(test_config=None):
    """Create and configure the questmaker app
    :param test_config: defines test or prod configuration
    :return: configured app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=path_to_db
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # main page
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
