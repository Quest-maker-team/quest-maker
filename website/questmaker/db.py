"""
Contains scripts to initialize db from cli, get access and close db connection
"""

import psycopg2
from psycopg2.extras import DictCursor
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Create new database connection or use current if exists
    :return: connection object
    """
    if 'db' not in g:
        name = current_app.config['DB_NAME']
        user = current_app.config['DB_USER']
        password = current_app.config['DB_PASSWORD']
        host = current_app.config['DB_HOST']
        port = current_app.config['DB_PORT']
        g.db = psycopg2.connect(dbname=name, user=user, password=password, host=host, port=port)
    return g.db


def close_db(e=None):
    """
    Close database connection if exists
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Open and execute file schema.sql with database initialization
    """
    with current_app.open_resource('schema.sql') as f:
        with get_db(), get_db().cursor() as cursor:
            cursor.execute(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Allows to init database from command line
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Add the opportunity to close db connection automatically when cleaning up after returning the response
    and add init db command that can be used with the flask command
    :param app: configured app
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def add_user(name, hash_psw, email):
    with get_db(), get_db().cursor() as cursor:
        cursor.execute('SELECT * from authors WHERE email = %s', (email, ))
        if cursor.fetchone():
            return False
        else:
            print(hash_psw)
            cursor.execute('INSERT INTO authors(name, hash_password, email) VALUES(%s, %s, %s)',
                           (name, hash_psw, email))
    return True


def get_user_by_id(user_id):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE id= %s', (user_id, ))
        res = cursor.fetchone()
        if not res:
            return False

    return res


def get_user_by_email(email):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE email= %s', (email, ))
        res = cursor.fetchone()
        if not res:
            return False

    return res
