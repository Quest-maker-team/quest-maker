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
        cursor.execute('SELECT quest_id, title, author_id, description, keyword, password, '
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
        cursor.execute('SELECT quest_id, keyword, title, password, '
                       'time_open, time_close, hidden, published '
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
        cursor.execute('SELECT tag_name '
                       'FROM tags JOIN quest_tags USING (tag_id)'
                       'WHERE quest_id = %s', (quest_id,))
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


def set_file(file):
    """
    Add rows to table files in database.
    :param file: file to load
    :return: True if success, False if not
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT f_type_id FROM file_types WHERE f_type_name = %s', (file.type,))
        type_id = cursor.fetchone()['f_type_id']
        if not (type_id is None):
            cursor.execute('INSERT INTO files (url_for_file,f_type_id) '
                           'VALUES (%s,%s) RETURNING f_id', (file.url, type_id))
            file.file_id = cursor.fetchone()['f_id']
            return True
        else:
            print("File type_id is None")
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
    :param published: string value: 'TRUE' or 'FALSE' - is quest already published
    :return: quest id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        if quest.id_in_db is not None:
            cursor.execute('DELETE FROM quests WHERE quest_id = %s', (quest.id_in_db,))
        cursor.execute('INSERT INTO quests (title, author_id, description, keyword, password, '
                       'time_open, time_close, lead_time, cover_url, hidden, published) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING quest_id',
                       (quest.title, quest.author_id, quest.description, quest.keyword,
                        quest.password, quest.time_open, quest.time_close, quest.lead_time,
                        quest.cover_url, str(quest.hidden).upper(), quest.published))
        quest.id_in_db = cursor.fetchone()['quest_id']
        return True


def set_rating(quest_id, rating: dict):
    """
    Add row to table ratings
    :param quest_id: quest id
    :param rating: data to load
    :return: rating id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO ratings (quest_id, one_star_amount, two_star_amount,'
                       'three_star_amount, four_star_amount, five_star_amount)'
                       'VALUES (%s, %s, %s, %s, %s, %s) RETURNING rating_id',
                       (quest_id, rating['one'], rating['two'],
                        rating['three'], rating['four'],
                        rating['five']))
        return cursor.fetchone()['rating_id']


def set_tags(tags, quest_id: int):
    """
    Add rows to table tags
    :param tags: quest tags
    :param quest_id: quest id
    :return: True if tags are loaded
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for tag in tags:
            cursor.execute('SELECT tag_id FROM tags WHERE tag_name = %s', (tag,))
            tag_id = cursor.fetchone()
            if tag_id is None:
                print("Creating new tag")
                cursor.execute('INSERT INTO tags (tag_name) '
                               'VALUES (%s) RETURNING tag_id', (tag,))
                tag_id = cursor.fetchone()
            cursor.execute('INSERT INTO quest_tags (quest_id, tag_id) '
                           'VALUES (%s, %s)', (quest_id, tag_id['tag_id']))

    return True


def get_question_type_id(q_type_name: str):
    """
    :param q_type_name: question type
    :return: question type id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT q_type_id FROM question_types WHERE q_type_name = %s', (q_type_name,))
        return cursor.fetchone()['q_type_id']


def set_place(place):
    """
    :param place: place to load
    :return: is transaction ok
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO places (coords, time_open, time_close, radius) '
                       'VALUES ( %s, %s, %s, %s) RETURNING place_id',
                       (place.coords, place.time_open, place.time_close, place.radius))
        place.place_id = cursor.fetchone()['place_id']
        return True


def get_draft(quest_id):
    """
    Get draft quest by related quest id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT draft_id, author_id, container FROM drafts WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_draft_for_update(draft_id):
    """
    Get draft quest by id and block row
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id, container FROM drafts WHERE draft_id = %s FOR UPDATE', (draft_id,))
        return cursor.fetchone()


def write_draft(author_id, container, quest_id):
    """
    Write draft to db
    :return: id of the new draft
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO drafts(author_id, container, quest_id) '
                       'VALUES (%s, %s, %s) RETURNING draft_id', (author_id, container, quest_id))
        return cursor.fetchone()['draft_id']


def update_draft(draft_id, container):
    """
    Update draft container
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE drafts SET container = %s WHERE draft_id = %s', (container, draft_id))


def remove_draft(quest_id):
    """
    Remove draft from db by related quest id
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('DELETE from drafts WHERE quest_id = %s', (quest_id,))


def check_uuid(uuid):
    """
    Return True if uuid is free else False
    """
    with get_db().cursor() as cursor:
        cursor.execute('SELECT quest_id FROM quests WHERE keyword = %s', (uuid,))
        return not cursor.fetchone()


def set_question(question, quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT q_type_id FROM question_types WHERE q_type_name = %s', (question.type,))
        type_id = cursor.fetchone()['q_type_id']
        if type_id is None:
            print("Type id is None")
            return False
        cursor.execute('INSERT INTO questions ( quest_id, question_text, q_type_id, pos_x, pos_y) '
                       'VALUES ( %s, %s, %s, %s, %s) RETURNING question_id',
                       (quest_id, question.text, type_id, question.pos_x, question.pos_y))
        question.question_id = cursor.fetchone()['question_id']
    return True


def set_quest_file(file, file_id):
    set_file(file)
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO quest_files (f_id, quest_id) '
                       'VALUES (%s, %s) RETURNING entry_id',
                       (file.file_id, file_id))
        file.entry_id = cursor.fetchone()['entry_id']
    return True


def set_question_file(file, question_id):
    set_file(file)
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO question_files (f_id, question_id) '
                       'VALUES (%s, %s) RETURNING entry_id',
                       (file.file_id, question_id))
        file.entry_id = cursor.fetchone()['entry_id']
    return True


def set_hint_file(file, hint_id):
    set_file(file)
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO hint_files (f_id, hint_id) '
                       'VALUES (%s, %s) RETURNING entry_id',
                       (file.file_id, hint_id))
        file.entry_id = cursor.fetchone()['entry_id']
    return True


def set_hint(hint, question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO hints (question_id, hint_text, fine)'
                       'VALUES (%s, %s, %s) RETURNING hint_id',
                       (question_id, hint.text, hint.fine))
        hint.hint_id = cursor.fetchone()['hint_id']
    return True


def set_movement(movement, question_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO movements ( question_id, place_id, next_question_id)'
                       'VALUES ( %s, %s, %s) RETURNING movement_id',
                       (question_id, movement.place.place_id, movement.next_question.question_id))
        movement.movement_id = cursor.fetchone()['movement_id']
    return True


def set_answer(answer, question_id):
    print("Setting answer, next_q_id=", answer.next_question.question_id)
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO answer_options (question_id, option_text, points, '
                       'next_question_id) '
                       'VALUES ( %s, %s, %s, %s) RETURNING option_id',
                       (question_id, answer.text, answer.points,
                        answer.next_question.question_id))
        answer.answer_option_id = cursor.fetchone()['option_id']
    return True


def get_tags():
    """
    Return all tags that contain substring
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT tag_name FROM tags")
        return cursor.fetchall()


def get_quest_from_catalog(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM quests_catalog WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_quests_from_catalog(limit, offset, sort_key, order, author, tags):
    """
    Select quests for catalog
    """
    query = 'SELECT * FROM quests_catalog '
    params = []
    if tags:
        tags_str = ', '.join("'" + tag + "'" for tag in tags)
        query += 'WHERE (SELECT COUNT(tag_id) FROM quests ' \
                 'JOIN quest_tags USING (quest_id) JOIN tags USING (tag_id) ' \
                 f'WHERE tag_name IN ({tags_str}) ' \
                 'GROUP BY quest_id) ' \
                 ' = %s '
        params.append(len(tags))
        if author:
            query += ' AND author = %s '
            params.append(author)
    else:
        if author:
            query += ' WHERE author = %s '
            params.append(author)

    if sort_key == 'id':
        query += f' ORDER BY quest_id '
    elif sort_key == 'rating':
        query += f' ORDER BY rating '
    elif sort_key == 'title':
        query += f' ORDER BY title '
    else:
        return

    query += f' {order} LIMIT {limit} OFFSET {offset}'

    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
