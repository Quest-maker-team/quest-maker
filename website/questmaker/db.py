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


@click.command('test-excursion')
@with_appcontext
def load_test_db_command():
    """
    Allows to load test database from command line
    """
    with current_app.open_resource('tests/excursion.sql') as f:
        with get_db(), get_db().cursor() as cursor:
            cursor.execute(f.read().decode('utf8'))
            cursor.execute('SELECT * FROM quests')
            click.echo(cursor.fetchall())
    click.echo('Test database loaded')


def print_quest(file, quest):
    import sys

    sys.stdout = open(file, "w")
    sys.stdout.reconfigure(encoding='utf-8')
    print('Quest info:')
    print(quest.title)
    print(quest.hidden)
    print(quest.tags)
    print(quest.rating)
    print(quest.description)
    print('Quest files:')
    for f in quest.files:
        print('\t', f.type)
        print('\t', f.url[:5])

    from queue import Queue
    qu = Queue()
    qu.put(quest.first_question)
    visited = []
    while not qu.empty():
        q = qu.get()
        if q in visited:
            continue
        else:
            visited.append(q)
        print('Question info:')
        print(q.type)
        print(q.text)
        print('Hints:')
        for hint in q.hints:
            print('\t', hint.text)
            print('\t', hint.fine)
            print('\t', 'Hint files:')
            for f in hint.files:
                print('\t\t', f.type)
                print('\t\t', f.url[:5])

        print('Question files:')
        for f in q.files:
            print('\t', f.type)
            print('\t', f.url[:5])

        if q.type == 'movement':
            print('Movements:')
            for move in q.movements:
                print('\t', move.place.coords, move.place.radius)
                if move.next_question:
                    qu.put(move.next_question)
        else:
            print('Answers:')
            for a in q.answers:
                print('\t', a.text)
                print('\t', a.points)
                if q.type == 'start':
                    for move in q.movements:
                        print('\t', move.place.coords, move.place.radius)
                if a.next_question:
                    qu.put(a.next_question)

    sys.stdout = sys.__stdout__


@click.command('test-loading')
@with_appcontext
def test_loading_to_and_from_db_command():
    """
    Allows to load data from classes and load it to
    new quest from command line
    """
    from .quest import Quest, Author
    quest = Quest.from_db(1)
    print_quest('quest1.txt', quest)

    author = Author("", "", "", "author", "")
    author.to_db()
    quest.to_db(author)

    quest = Quest.from_db(2)
    print_quest('quest2.txt', quest)

    click.echo('Test completed')


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
    :return: dictionary src of line from table authors
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
    :return: dictionary src of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from authors WHERE email= %s', (email,))
        res = cursor.fetchone()
        if not res:
            return False

    return res


def get_quest(quest_id):
    """
    Load quest from table quests (with author name instead of author id)
    :param quest_id: quest id in database
    :return: dictionary with table attrs as keys
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT title, author_id, description, password, '
                       'time_open, time_close, lead_time, cover_url, hidden '
                       'FROM quests '
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_quests_by_author_id(author_id):
    """
    Load quests info for personal catalog from table quests by author id
    :param author_id: author id in database
    :return: list of dictionaries with attrs as keys
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT quest_id, title, password, '
                       'time_open, time_close, hidden '
                       'FROM quests '
                       'WHERE author_id = %s', (author_id,))
        return cursor.fetchall()


def get_quest_tags(quest_id):
    """
    Load tags related with quest
    :param quest_id: quest id in database
    :return: list of dictionaries with key tag_name
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT tag_name FROM tags WHERE quest_id = %s', (quest_id,))
        return cursor.fetchall()


def get_quest_files(quest_id):
    """
    Load files related with quest
    :param quest_id: quest id in database
    :return: list of dictionaries with keys url_for_file and f_type_name
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN quest_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchall()


def get_quest_rating(quest_id):
    """
    Load quest rating
    :param quest_id: quest id in database
    :return: dictionary with keys one, two, free, four, five
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT one_star_amount AS one, '
                       'two_star_amount AS two, '
                       'three_star_amount AS three, '
                       'four_star_amount AS four, '
                       'five_star_amount AS five '
                       'FROM ratings WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_start_question_id(quest_id):
    """
    Get id of fictive start question
    :param quest_id: quest id in database
    :return: start question id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_id FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE quest_id = %s AND q_type_name = \'start\'', (quest_id,))
        return cursor.fetchone()


def get_question(question_id):
    """
    Load question from database by id with type name instead of type id
    :param question_id: question id in database
    :return: dictionary with q_type_name instead of q_type_id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT question_text, q_type_name, pos_x, pos_y FROM questions '
                       'JOIN question_types USING (q_type_id) '
                       'WHERE question_id = %s', (question_id,))
        return cursor.fetchone()


def get_question_files(question_id):
    """
    Load files related with quest
    :param question_id: question id in database
    :return: list of dictionaries with keys url_for_file and f_type_name
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN question_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_hints_ids(question_id):
    """
    Get hint ids related with question
    :param question_id: question id in database
    :return: list of dictionaries with key hint_id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT hint_id FROM hints WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_answer_options_ids(question_id):
    """
    Get answer option ids related with question
    :param question_id: question id in database
    :return: list of dictionaries with key option_id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_id FROM answer_options WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_question_movements_ids(question_id):
    """
    Get movement ids related with question
    :param question_id: question id in database
    :return: list of dictionaries with key movement_id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT movement_id FROM movements WHERE question_id = %s', (question_id,))
        return cursor.fetchall()


def get_answer_option(answer_option_id):
    """
   Load answer option from database
   :param answer_option_id: answer option id in database
   :return: dictionary with keys as same as in table answer_options
   """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT option_text, points, next_question_id '
                       'FROM answer_options WHERE option_id = %s', (answer_option_id,))
        return cursor.fetchone()


def get_movement(movement_id):
    """
   Load movement from database
   :param movement_id: movement id in database
   :return: dictionary with keys as same as in table movements
   """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT place_id, next_question_id '
                       'FROM movements WHERE movement_id = %s', (movement_id,))
        return cursor.fetchone()


def get_hint(hint_id):
    """
   Load hint from database
   :param hint_id: hint id in database
   :return: dictionary with keys as same as in table hints
   """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT hint_text, fine '
                       'FROM hints WHERE hint_id = %s', (hint_id,))
        return cursor.fetchone()


def get_hint_files(hint_id):
    """
    Load files related with quest
    :param hint_id: hint id in database
    :return: list of dictionaries with keys url_for_file and f_type_name
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT url_for_file, f_type_name '
                       'FROM files '
                       'JOIN hint_files USING (f_id) '
                       'JOIN file_types USING (f_type_id) '
                       'WHERE hint_id = %s', (hint_id,))
        return cursor.fetchall()


def get_place(place_id):
    """
    Load place from database
    :param place_id: place id in database
    :return: dictionary with keys as same as in table places
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT coords, time_open, time_close, radius '
                       'FROM places WHERE place_id = %s', (place_id,))
        return cursor.fetchone()


def get_file_types():
    """
    Load list of supported file types
    """
    with get_db().cursor() as cursor:
        cursor.execute('SELECT f_type_name FROM file_types')
        return [row[0] for row in cursor.fetchall()]


def get_question_types():
    """
    Load list of supported question types
    """
    with get_db().cursor() as cursor:
        cursor.execute('SELECT q_type_name FROM question_types')
        return [row[0] for row in cursor.fetchall()]


def set_file(file, cursor):
    """
    Add rows to table files in database.
    :param file: file to load
    :param cursor: cursor to loading file
    :return: file id if success, False if not
    """
    if cursor is None:
        ids = []
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute('SELECT f_type_id FROM file_types WHERE f_type_name = %s', (file.type,))
            type_id = cursor.fetchone()['f_type_id']
            if not (type_id is None):
                cursor.execute('INSERT INTO files (url_for_file,f_type_id) '
                               'VALUES (%s,%s) RETURNING f_id', (file.url, type_id))
                return cursor.fetchone()['f_id']
            else:
                return False
    else:
        ids = []
        cursor.execute('SELECT f_type_id FROM file_types WHERE f_type_name = %s', (file.type,))
        type_id = cursor.fetchone()['f_type_id']
        if not (type_id is None):
            cursor.execute('INSERT INTO files (url_for_file,f_type_id) '
                           'VALUES (%s,%s) RETURNING f_id', (file.url, type_id))
            return cursor.fetchone()['f_id']
        else:
            return False


def get_author_id_by_email(email: str):
    """
    Method to get author_id by email
    :param email: email
    :return: author id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id FROM authors WHERE email = %s ', (email,))
        author_id = 1
        if cursor.fetchone():
            author_id = cursor.fetchone()['author_id']
        return author_id


def set_author(author):
    """
    Add row in table authors from Author object
    :param author: Author object to loa
    :return: author id if it exists, False if not
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT status_id FROM statuses WHERE status_name = %s', (author.status,))
        status_id = cursor.fetchone()['status_id']
        if status_id:
            cursor.execute('INSERT INTO authors (name, password, email, status_id, avatar_url)'
                           'VALUES (%s,%s,%s,%s,%s) RETURNING author_id',
                           (author.name, author.password, author.email), status_id, author.avatar_url)
            return cursor.fetchone()['author_id']
        else:
            return False


def set_quest(quest):
    """
    Add row to table quest in database from Quest object and author email
    :param quest: quest to load in database
    :return: quest id
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        if quest.id_in_db is not None:
            cursor.execute('DELETE FROM quests WHERE quest_id = %s', (quest.id_in_db, ))
        cursor.execute('INSERT INTO quests (title, author_id, description, password, '
                       'time_open, time_close, lead_time, cover_url, hidden) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING quest_id',
                       (quest.title, quest.author_id, quest.description,
                        quest.password, quest.time_open, quest.time_close, quest.lead_time,
                        quest.cover_url, str(quest.hidden).upper()))
        return cursor.fetchone()['quest_id']


def set_rating(quest_id, rating: dict):
    """
    Add row to table ratings
    :param quest_id: quest id
    :param rating: data to load
    :return: rating id
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
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
    :param quest: quest
    :param quest_id: quest id
    :return: True if tags are loaded
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for tag in quest.tags:
            cursor.execute('INSERT INTO tags (quest_id, tag_name) '
                           'VALUES (%s, %s)', (quest_id, tag))

    return True


def set_quest_files(files: list, quest_id: int):
    """
    Add rows to table quest_files
    :param files: list of files to load
    :param quest_id: quest id
    :return: list correctly loaded files
    """
    ids = []
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for file in files:
            file_id = set_file(file, cursor)
            cursor.execute('INSERT INTO quest_files (f_id, quest_id) '
                           'VALUES (%s, %s)', (file_id, quest_id))
            ids.append(file)

    return ids


def get_question_type_id(q_type_name: str):
    """
    :param q_type_name: question type
    :return: question type id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT q_type_id FROM question_types WHERE q_type_name = %s', (q_type_name,))
        return cursor.fetchone()['q_type_id']


def set_place(place, cursor):
    """
    :param place: place to load
    :param cursor: our connection to database, if None create new
    :return:place id
    """

    if not cursor:
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute('INSERT INTO places (coords, time_open, time_close, radius)'
                           'VALUES (%s, %s, %s, %s) RETURNING place_id',
                           (place.coords, place.time_open, place.time_close, place.radius))
            return cursor.fetchone()['place_id']
    else:
        cursor.execute('INSERT INTO places (coords, time_open, time_close, radius)'
                       'VALUES (%s, %s, %s, %s) RETURNING place_id',
                       (place.coords, place.time_open, place.time_close, place.radius))
        return cursor.fetchone()['place_id']


def create_new_question(question, quest_id, cursor=None):
    """
    Add new row to table questions from Question object
    :param question: question to witch hints are loaded
    :param quest_id: quest id
    :param cursor: our connection to database, if None create new
    :return: question id
    """
    if not cursor:
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute('INSERT INTO questions (quest_id, question_text, q_type_id)'
                           'VALUES (%s, %s, %s) RETURNING question_id',
                           (quest_id, question.text, get_question_type_id(question.type)))
            id = cursor.fetchone()['question_id']
            create_question_files(question, id, cursor)
            create_hints(question, id, cursor)
            return id
    else:
        cursor.execute('INSERT INTO questions (quest_id, question_text, q_type_id)'
                       'VALUES (%s, %s, %s) RETURNING question_id',
                       (quest_id, question.text, get_question_type_id(question.type)))
        id = cursor.fetchone()['question_id']
        create_question_files(question, id, cursor)
        create_hints(question, id, cursor)
        return id


def create_question_files(question, question_id: int, cursor):
    """
    Load question files to database
    :param question: question to witch hints are loaded
    :param question_id: question id
    :param cursor: our connection to database, if None create new
    :return: list of question files
    """
    if cursor is None:
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            ids = []
            for file in question.files:
                file_id = set_file(file, cursor)
                ids.append(file)
                cursor.execute('INSERT INTO question_files (f_id, question_id) '
                               'VALUES (%s, %s)', (file_id, question_id))
            return ids
    else:
        ids = []
        for file in question.files:
            file_id = set_file(file, cursor)
            ids.append(file)
            cursor.execute('INSERT INTO question_files (f_id, question_id) '
                           'VALUES (%s, %s)', (file_id, question_id))
        return ids


def create_hints(question, question_id: int, cursor):
    """
    Add rows to hints and hint_files tables
    :param question: question to witch hints are loaded
    :param question_id: question id
    :param cursor: our connection to database, if None create new
    :return: list of hint files
    """
    if not cursor:
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            ids = []
            for hint in question.hints:
                cursor.execute('INSERT INTO hints (question_id, hint_text, fine)'
                               'VALUES (%s, %s, %s) RETURNING hint_id',
                               (question_id, hint.text, hint.fine))
                hint_id = cursor.fetchone()['hint_id']
                for hint_file in hint.files:
                    hint_file_id = set_file(hint_file, cursor)
                    cursor.execute('INSERT INTO hint_files (f_id, hint_id)'
                                   'VALUES (%s, %s)', (hint_file_id, hint_id))
                    ids.append(hint_file)
        return ids
    else:
        ids = []
        for hint in question.hints:
            cursor.execute('INSERT INTO hints (question_id, hint_text, fine)'
                           'VALUES (%s, %s, %s) RETURNING hint_id',
                           (question_id, hint.text, hint.fine))
            hint_id = cursor.fetchone()['hint_id']
            for hint_file in hint.files:
                hint_file_id = set_file(hint_file, cursor)
                cursor.execute('INSERT INTO hint_files (f_id, hint_id)'
                               'VALUES (%s, %s)', (hint_file_id, hint_id))
                ids.append(hint_file)
    return ids


def set_questions(used_files: list, question, quest_id: int, places: dict, question_id, questions: dict, answers: dict,
                  movements: dict, cursor=None):
    """
    Add rows to questions table, using recursion to bypass the entire graph of questions
    :param used_files: already load files
    :param question: current question
    :param quest_id: id of quest
    :param places: already load places
    :param question_id: current question id
    :param questions: already load questions
    :param answers: already load answers
    :param movements: already load movements
    :param cursor: to avoid re-connection to database
    :return: True if all is ok
    """
    if not cursor:
        with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            if question.type == 'start':
                for movement in question.movements:
                    if movement.place not in places.keys():
                        places[movement.place] = set_place(movement.place, cursor)
                    if movement.next_question not in questions.keys():
                        next_question_id = create_new_question(movement.next_question, quest_id, cursor)
                        questions[movement.next_question] = next_question_id
                    else:
                        next_question_id = questions[movement.next_question]
                    if movement not in movements.keys():
                        cursor.execute('INSERT INTO movements (question_id, place_id, next_question_id)'
                                       'VALUES (%s, %s, %s) RETURNING movement_id',
                                       (question_id, places[movement.place], next_question_id))
                        movements[movement] = cursor.fetchone()['movement_id']
                for answer in question.answers:
                    if answer.next_question not in questions.keys():
                        next_question_id = create_new_question(answer.next_question, quest_id, cursor)
                        questions[answer.next_question] = next_question_id
                    else:
                        next_question_id = questions[answer.next_question]
                    if answer not in answers:
                        cursor.execute('INSERT INTO answer_options (question_id, option_text, points, next_question_id)'
                                       'VALUES (%s, %s, %s, %s) RETURNING option_id',
                                       (question_id, answer.text, answer.points, next_question_id))
                        answers[answer] = cursor.fetchone()['option_id']
                set_questions(used_files, movement.next_question, quest_id, places, next_question_id, questions,
                              answers, movements, cursor)

            else:
                return True
    else:
        if question.type == 'movement':
            for movement in question.movements:
                if movement.place not in places.keys():
                    places[movement.place] = set_place(movement.place, cursor)
                if movement.next_question not in questions.keys():
                    next_question_id = create_new_question(movement.next_question, quest_id, cursor)
                    questions[movement.next_question] = next_question_id
                else:
                    next_question_id = questions[movement.next_question]
                if movement not in movements.keys():
                    cursor.execute('INSERT INTO movements (question_id, place_id, next_question_id)'
                                   'VALUES (%s, %s, %s) RETURNING movement_id',
                                   (question_id, places[movement.place], next_question_id))
                    movements[movement] = cursor.fetchone()['movement_id']
                    set_questions(used_files, movement.next_question, quest_id, places, next_question_id, questions,
                                  answers, movements, cursor)
        elif question.type != 'end':
            for answer in question.answers:
                if answer.next_question not in questions.keys():
                    next_question_id = create_new_question(answer.next_question, quest_id, cursor)
                    questions[answer.next_question] = next_question_id
                else:
                    next_question_id = questions[answer.next_question]
                if answer not in answers:
                    cursor.execute('INSERT INTO answer_options (question_id, option_text, points, next_question_id)'
                                   'VALUES (%s, %s, %s, %s) RETURNING option_id',
                                   (question_id, answer.text, answer.points, next_question_id))
                    answers[answer] = cursor.fetchone()['option_id']
                    set_questions(used_files, answer.next_question, quest_id, places, next_question_id, questions,
                                  answers, movements, cursor)

        else:
            return True


def get_draft(draft_id):
    """
    Get draft quest by id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id, container FROM drafts WHERE draft_id = %s', (draft_id,))
        return cursor.fetchone()


def get_drafts_by_author_id(author_id):
    """
    Get drafts quest by author id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT draft_id, container FROM drafts WHERE author_id = %s', (author_id,))
        return cursor.fetchall()


def get_draft_for_update(draft_id):
    """
    Get draft quest by id and block row
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id, container FROM drafts WHERE draft_id = %s FOR UPDATE', (draft_id,))
        return cursor.fetchone()


def write_draft(author_id, container):
    """
    Write draft to db
    :return: id of the new draft
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO drafts(author_id, container) '
                       'VALUES (%s, %s) RETURNING draft_id', (author_id, container))
        return cursor.fetchone()['draft_id']


def update_draft(draft_id, container):
    """
    Update draft container
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE drafts SET container = %s WHERE draft_id = %s', (container, draft_id))


def remove_draft(draft_id):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('DELETE from drafts WHERE draft_id = %s', (draft_id, ))
