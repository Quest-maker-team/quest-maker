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
    """
    Add user to table authors
    :param name: user name
    :param hash_psw: hash of password
    :param email: user email
    :return: True if success or False if user is already exists
    """
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
    """
    Find user in table authors by id
    :param user_id: user id
    :return: dictionary view of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE id= %s', (user_id, ))
        res = cursor.fetchone()
        if not res:
            return False

    return res


def get_user_by_email(email):
    """
    Find user in table authors by email
    :param email: user email
    :return: dictionary view of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE email= %s', (email, ))
        res = cursor.fetchone()
        if not res:
            return False

    return res


def get_quest(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT title, authors.name AS author, description, quests.password AS password, '
                       'time_open, time_close, lead_time, cover_url, hidden '
                       'FROM quests '
                       'JOIN authors USING (author_id) '
                       'WHERE quest_id = %s', (quest_id, ))
        return cursor.fetchone()


def get_quest_tags(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT tag_name FROM tags WHERE quest_id = %s', (quest_id, ))
        return cursor.fetchall()


def get_quest_files(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN quest_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE quest_id = %s', (quest_id, ))
        return cursor.fetchall()


def get_quest_rating(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT one_star_amount AS one, '
                       'two_star_amount AS two, '
                       'three_star_amount AS three, '
                       'four_star_amount AS four, '
                       'five_star_amount AS five '
                       'FROM ratings WHERE quest_id = %s', (quest_id, ))
        return cursor.fetchone()


def get_start_question_id(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_id FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE quest_id = %s AND q_type_name = \'start\'', (quest_id, ))
        return cursor.fetchone()


def get_question(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_text, q_type_name FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE question_id = %s', (question_id, ))
        return cursor.fetchone()


def get_question_files(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN question_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE question_id = %s', (question_id, ))
        return cursor.fetchall()


def get_question_hints_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT hint_id FROM hints WHERE question_id = %s', (question_id, ))
        return cursor.fetchall()


def get_question_answer_options_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_id FROM answer_options WHERE question_id = %s', (question_id, ))
        return cursor.fetchall()


def get_question_movements_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT movement_id FROM movements WHERE question_id = %s', (question_id, ))
        return cursor.fetchall()


def get_answer(answer_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_text, points, next_question_id '
                       'FROM answer_options WHERE option_id = %s', (answer_id, ))
        return cursor.fetchone()


def get_movement(movement_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT place_id, next_question_id '
                       'FROM movements WHERE movement_id = %s', (movement_id, ))
        return cursor.fetchone()


def get_hint(hint_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT hint_text, fine '
                       'FROM hints WHERE hint_id = %s', (hint_id,))
        return cursor.fetchone()


def get_hint_files(hint_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN hint_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE hint_id = %s', (hint_id,))
        return cursor.fetchall()


def get_place(place_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT coords, time_open, time_close, radius '
                       'FROM places WHERE place_id = %s', (place_id,))
        return cursor.fetchone()
