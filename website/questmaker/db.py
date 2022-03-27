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


@click.command('test-museum')
@with_appcontext
def load_test_db_command():
    """
    Allows to load test database from command line
    """
    with current_app.open_resource('tests/museum.sql') as f:
        with get_db(), get_db().cursor() as cursor:
            cursor.execute(f.read().decode('utf8'))
            cursor.execute('SELECT * FROM quests')
            click.echo(cursor.fetchall())
    click.echo('Test database loaded')


@click.command('test-loading')
@with_appcontext
def test_loading_to_and_from_db_command():
    """
    Allows to load data from classes and load it to
    new quest from command line
    """
    from .quest import Quest, Author
    quest = Quest.from_db(1)
    author = Author("", "", "", "author", "")
    author.to_db()
    quest.to_db(author)
    click.echo('Test complited')


def init_app(app):
    """
    Add the opportunity to close db connection automatically when cleaning up after returning the response
    and add init db command that can be used with the flask command
    :param app: configured app
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_test_db_command)
    app.cli.add_command(test_loading_to_and_from_db_command)


def add_user(name, hash_psw, email):
    """
    Add user to table authors
    :param name: user name
    :param hash_psw: hash of password
    :param email: user email
    :return: True if success or False if user is already exists
    """
    with get_db(), get_db().cursor() as cursor:
        cursor.execute('SELECT * from authors WHERE email = %s', (email,))
        if cursor.fetchone():
            return False
        else:
            print(hash_psw)
            cursor.execute('INSERT INTO authors(name, password, email, status_id) '
                           'VALUES(%s, %s, %s, '
                           '(SELECT status_id FROM statuses WHERE status_name = \'author\'))',
                           (name, hash_psw, email))
    return True


def get_author_by_id(author_id):
    """
    Find user in table authors by id
    :param author_id: user id
    :return: dictionary view of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE author_id= %s', (author_id,))
        res = cursor.fetchone()
        if not res:
            return False

    return res


def get_author_by_email(email):
    """
    Find user in table authors by email
    :param email: user email
    :return: dictionary view of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE email= %s', (email,))
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
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_quest_tags(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT tag_name FROM tags WHERE quest_id = %s', (quest_id,))
        return cursor.fetchall()


def get_quest_files(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN quest_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchall()


def get_quest_rating(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT one_star_amount AS one, '
                       'two_star_amount AS two, '
                       'three_star_amount AS three, '
                       'four_star_amount AS four, '
                       'five_star_amount AS five '
                       'FROM ratings WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_start_question_id(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_id FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE quest_id = %s AND q_type_name = \'start\'', (quest_id,))
        return cursor.fetchone()


def get_question(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_text, q_type_name FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE question_id = %s', (question_id,))
        return cursor.fetchone()


def get_question_files(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN question_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_hints_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT hint_id FROM hints WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_answer_options_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_id FROM answer_options WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_movements_ids(question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT movement_id FROM movements WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_answer_option(answer_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_text, points, next_question_id '
                       'FROM answer_options WHERE option_id = %s', (answer_id,))
        return cursor.fetchone()


def get_movement(movement_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT place_id, next_question_id '
                       'FROM movements WHERE movement_id = %s', (movement_id,))
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


def set_file(file):
    """
    Add rows to table files in database.
    """
    ids = []
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT f_type_id FROM file_types WHERE f_type_name = %s', (file.type,))
        type_id = cursor.fetchone()['f_type_id']
        if type_id:
            cursor.execute('INSERT INTO files (url_for_file,f_type_id) '
                           'VALUES (%s,%s) RETURNING f_id', (file.url, type_id))
            return cursor.fetchone()['f_id']
        else:
            return False


def get_author_id_by_email(email: str):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id FROM authors WHERE email = %s ', (email,))
        author_id = 1
        if cursor.fetchone():
            author_id = cursor.fetchone()['author_id']
        return author_id


def set_author(author):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT status_id FROM statuses WHERE status_name = %s', (author.status,))
        status_id = cursor.fetchone()['status_id']
        if status_id:
            cursor.execute('INSERT INTO authors (name, password, email, status_id, avatar_url)'
                           'VALUES (%s,%s,%s,%s,%s) RETURNING author_id',
                           (author.name, author.password, author.email), status_id, author.avatar_url)
            return cursor.fetchone()['author_id']
        else:
            return False


def set_quest(quest, author_email):
    """
    Add row to table quest in database
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO quests (title, author_id, description, password, '
                       'time_open, time_close, lead_time, cover_url, hidden) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING quest_id',
                       (quest.title, get_author_id_by_email(author_email), quest.description,
                        quest.password, quest.time_open, quest.time_close, quest.lead_time,
                        quest.cover_url, str(quest.hidden).upper()))
        return cursor.fetchone()['quest_id']


def set_rating(quest_id, rating: dict):
    """
    Add row to table ratings
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO ratings (quest_id, one_star_amount, two_star_amount,'
                       'three_star_amount, four_star_amount, five_star_amount)'
                       'VALUES (%s, %s, %s, %s, %s, %s) RETURNING rating_id',
                       (quest_id, rating['one'], rating['two'],
                        rating['three'], rating['four'],
                        rating['five']))

        return cursor.fetchone()['rating_id']


def set_tags(quest, quest_id: int):
    """
    Add rows to table tags
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for tag in quest.tags:
            cursor.execute('INSERT INTO tags (quest_id, tag_name) '
                           'VALUES (%s, %s)', (quest_id, tag))

    return True


def set_quest_files(files: list, quest_id: int):
    """
    Add rows to table quest_files
    """
    ids = []
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for file in files:
            file_id = set_file(file)
            cursor.execute('INSERT INTO quest_files (f_id, quest_id) '
                           'VALUES (%s, %s)', (file_id, quest_id))
            ids.append(file)

    return ids


def get_question_type_id(q_type_name: str):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT q_type_id FROM question_types WHERE q_type_name = %s', (q_type_name,))
        return cursor.fetchone()['q_type_id']


def set_place(place):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO places (coords, time_open, time_close, radius)'
                       'VALUES (%s, %s, %s, %s) RETURNING place_id',
                       (place.coords, place.time_open, place.time_close, place.radius))
        return cursor.fetchone()['place_id']


def create_new_question(question, quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO questions (quest_id, question_text, q_type_id)'
                       'VALUES (%s, %s, %s) RETURNING question_id',
                       (quest_id, question.text, get_question_type_id(question.type)))
        return cursor.fetchone()['question_id']


def create_question_files(question, question_id: int):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        ids = []
        for file in question.files:
            file_id = set_file(file)
            ids.append(file)
            cursor.execute('INSERT INTO question_files (f_id, question_id)'
                           'VALUES (%s, %s)', (file_id, question_id))
        return ids


def create_hints(question, question_id: int):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        ids = []
        for hint in question.hints:
            cursor.execute('INSERT INTO hints (question_id, hint_text, fine)'
                           'VALUES (%s, %s, %s) RETURNING hint_id',
                           (question_id, hint.text, hint.fine))
            hint_id = cursor.fetchone()['hint_id']
            for hint_file in hint.files:
                hint_file_id = set_file(hint_file)
                cursor.execute('INSERT INTO hint_files (f_id, hint_id)'
                               'VALUES (%s, %s)', (hint_file_id, hint_id))
                ids.append(hint_file)
    return ids


def set_questions(used_files: list, question, quest_id: int, places: dict, question_id, questions: dict, answers: dict,
                  movements: dict):
    """
    Add rows to questions table
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        if question not in questions.keys():
            used_files.append(create_question_files(question, question_id))
            used_files.append(create_hints(question, question_id))
        if question.type == 'movement':
            for movement in question.movements:
                if movement.place not in places:
                    places[movement] = set_place(movement.place)
                if movement.next_question not in questions.keys():
                    next_question_id = create_new_question(movement.next_question, quest_id)
                    questions[movement.next_question] = next_question_id
                else:
                    next_question_id = questions[movement.next_question]
                if movement not in movements.keys():
                    cursor.execute('INSERT INTO movements (question_id, place_id, next_question_id)'
                                   'VALUES (%s, %s, %s) RETURNING movement_id',
                                   (question_id, places[movement], next_question_id))
                    movements[movement] = cursor.fetchone()['movement_id']
                    set_questions(used_files, movement.next_question, quest_id, places, next_question_id, questions,
                                  answers, movements)
        elif question.type != 'end':
            for answer in question.answers:
                if answer.next_question not in questions.keys():
                    next_question_id = create_new_question(answer.next_question, quest_id)
                    questions[answer.next_question] = next_question_id
                else:
                    next_question_id = questions[answer.next_question]
                if answer not in answers:
                    cursor.execute('INSERT INTO answer_options (question_id, option_text, points, next_question_id)'
                                   'VALUES (%s, %s, %s, %s) RETURNING option_id',
                                   (question_id, answer.text, answer.points, next_question_id))
                    answers[answer] = cursor.fetchone()['option_id']
                    set_questions(used_files, answer.next_question, quest_id, places, next_question_id, questions,
                                  answers, movements)

        else:
            return True
