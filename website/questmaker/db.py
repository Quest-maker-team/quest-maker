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
            cursor.execute('SELECT * FROM quest')
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
                print('\t', move.place.coord_x, move.place.coord_y, move.place.radius)
                if move.next_question:
                    qu.put(move.next_question)
        else:
            print('Answers:')
            for a in q.answers:
                print('\t', a.text)
                print('\t', a.points)
                if q.type == 'start':
                    for move in q.movements:
                        print('\t', move.place.coord_x, move.place.coord_y, move.place.radius)
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
    # app.cli.add_command(load_test_db_command)
    # app.cli.add_command(test_loading_to_and_from_db_command)


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
            cursor.execute('SELECT * FROM quest')
            click.echo(cursor.fetchall())
    click.echo('Test database loaded')

def get_quest(quest_id):
    """
    Load quest from table quests (with author name instead of author id)
    :param quest_id: quest id in database
    :return: dictionary with table attrs as keys
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT quest_id, title, author_id, description, keyword, password, '
                       'time_open, time_close, lead_time, cover_path, periodicity, hidden, published  '
                       'FROM quest '
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()

def get_quest_tags(quest_id):
    """
    Load tags related with quest
    :param quest_id: quest id in database
    :return: list of dictionaries with key tag_name
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT tag_name '
                       'FROM tag JOIN quest_tag USING (tag_id)'
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
                       'FROM rating WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()
        
def get_blocks(quest_id):
    """
    Load blocks from database by blocks id with type name instead of type id
    :param quest_id: quest id in database
    :return: dictionary with q_type_name instead of q_type_id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT block_id, block_text, block_type_name, pos_x, pos_y, next_block_id FROM block '
                       'JOIN block_type USING (block_type_id) '
                       'WHERE quest_id = %s', (quest_id,))
        return cursor.fetchall()
    
def get_draft(quest_id):
    """
    Get draft quest by related quest id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT draft_id, author_id, container_path FROM draft WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()


def get_draft_for_update(draft_id):
    """
    Get draft quest by id and block row
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT author_id, container_path FROM draft WHERE draft_id = %s FOR UPDATE', (draft_id,))
        return cursor.fetchone()


def write_draft(author_id, container, quest_id):
    """
    Write draft to db
    :return: id of the new draft
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO draft(author_id, container_path, quest_id) '
                       'VALUES (%s, %s, %s) RETURNING draft_id', (author_id, container, quest_id))
        return cursor.fetchone()['draft_id']


def update_draft(draft_id, container):
    """
    Update draft container
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE draft SET container_path = %s WHERE draft_id = %s', (container, draft_id))


def remove_draft(quest_id):
    """
    Remove draft from db by related quest id
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('DELETE from draft WHERE quest_id = %s', (quest_id,))

def get_quests_by_author_id(author_id):
    """
    Load quests info for personal catalog from table quests by author id
    :param author_id: author id in database
    :return: list of dictionaries with attrs as keys
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT quest_id, keyword, title, password, '
                       'time_open, time_close, hidden, published, periodicity '
                       'FROM quest '
                       'WHERE author_id = %s', (author_id,))
        return cursor.fetchall()
    
def get_author_by_id(author_id):
    """
    Find user in table authors by id
    :param author_id: user id
    :return: dictionary src of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from author WHERE author_id= %s', (author_id,))
        res = cursor.fetchone()
        if not res:
            return False

    return res

def add_user(name, hash_psw, email):
    """
    Add user to table authors
    :param name: user name
    :param hash_psw: hash of password
    :param email: user email
    :return: True if success or False if user is already exists
    """
    with get_db(), get_db().cursor() as cursor:
        cursor.execute('SELECT * from author WHERE email = %s', (email,))
        if cursor.fetchone():
            return False
        else:
            print(hash_psw)
            cursor.execute('INSERT INTO author(name, password, email, status_id) '
                           'VALUES(%s, %s, %s, '
                           '(SELECT status_id FROM status WHERE status_name = \'author\'))',
                           (name, hash_psw, email))
    return True

def get_author_by_email(email):
    """
    Find user in table authors by email
    :param email: user email
    :return: dictionary src of line from table authors
    """
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from author WHERE email= %s', (email,))
        res = cursor.fetchone()

    return res

def remove_quest(quest_id):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * from quest WHERE quest_id = %s', (quest_id,))
        if not cursor.fetchone():
            return False
        cursor.execute('DELETE from quest WHERE quest_id = %s', (quest_id,))
    return True

def get_quest_from_catalog(quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM quests_catalog WHERE quest_id = %s', (quest_id,))
        return cursor.fetchone()

def get_tags():
    """
    Return all tags that contain substring
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT tag_name FROM tag")
        return cursor.fetchall()

def get_quests_from_catalog(title, description, limit, offset, sort_key, order, author, tags):
    """
    Select quests for catalog
    """
    query = 'SELECT * FROM quests_catalog '
    params = []
    reg_title = f'%{title}%'
    reg_description = f'%{description}%'
    if tags:
        tags_str = ', '.join("'" + tag + "'" for tag in tags)
        query += 'JOIN (SELECT quest_id, COUNT(tag_id) AS tags_matched FROM quest ' \
                 'JOIN quest_tag USING (quest_id) JOIN tag USING (tag_id) ' \
                 f'WHERE tag_name IN ({tags_str}) ' \
                 'GROUP BY quest_id) AS matched USING (quest_id)' \
                 'WHERE tags_matched >= %s AND title LIKE %s  AND (description LIKE %s OR description IS NULL)'
        params.append(len(tags))
    else:
        query += 'WHERE title LIKE %s  AND (description LIKE %s OR description IS NULL)'

    params.append(reg_title)
    params.append(reg_description)

    if author:
        query += ' AND author = %s '
        params.append(author)

    if sort_key == 'id':
        query += f' ORDER BY quest_id '
    elif sort_key == 'rating':
        query += f' ORDER BY rating '
    elif sort_key == 'title':
        query += f' ORDER BY title '
    else:
        return

    query += f'{order}'

    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(query, tuple(params))
        res = cursor.fetchall()

    total = len(res)
    print(cursor.query)
    print(total, res)
    return total, res[offset:offset + limit]

def get_quests_num():
    with get_db().cursor() as cursor:
        cursor.execute('SELECT COUNT(quest_id) FROM quests_catalog')
        return cursor.fetchone()[0]
    
def check_uuid(uuid):
    """
    Return True if uuid is free else False
    """
    with get_db().cursor() as cursor:
        cursor.execute('SELECT quest_id FROM quest WHERE keyword = %s', (uuid,))
        return not cursor.fetchone()
    
def add_media(table_name: str, 
              media_path: str, 
              media_type_id: int,
              object_type: str,
              object_id: int) -> bool:
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'INSERT INTO {table_name} (media_path, media_type_id, {object_type}_id) '
                       'VALUES (%s, %s, %s)',
                       (media_path, media_type_id, object_id))
        
    return True

def add_answer(option_text: str, 
              points: float, 
              block_id: int):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'INSERT INTO answer_option (block_id, option_text, points) '
                       'VALUES (%s, %s, %s) RETURNING option_id',
                       (block_id, option_text, points))
        
        return cursor.fetchone()['option_id']
    
def add_place(latitude: float,
               longitude: float,
               radius: float, 
               time_open, 
               time_close, 
              block_id: int) -> bool:
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'INSERT INTO place (block_id, latitude, longitude, radius, time_open, time_close) '
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (block_id, latitude, longitude, radius, time_open, time_close))
        
    return True

def add_hint(text: str, 
              fine: float, 
              block_id: int):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(f'INSERT INTO hint (block_id, hint_text, fine) '
                       'VALUES (%s, %s, %s) RETURNING hint_id',
                       (block_id, text, fine))
        
        return cursor.fetchone()['hint_id']

def set_quest(quest):
    """
    Add row to table quest in database from Quest object and author email
    :param quest: quest to load in database
    :return: quest id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        if quest.id is not None:
            cursor.execute('DELETE FROM quest WHERE quest_id = %s', (quest.id,))
        print(quest.title, quest.author_id, quest.keyword)
        cursor.execute('INSERT INTO quest (title, author_id, description, keyword, password, '
                    'cover_path, hidden, published) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING quest_id',
                    (quest.title, quest.author_id, quest.description, quest.keyword,
                        quest.password, quest.cover_path, quest.hidden, quest.published))
        
        
        quest.id = cursor.fetchone()['quest_id']
        return True

    
def set_tags(tags, quest_id: int):
    """
    Add rows to table tags
    :param tags: quest tags
    :param quest_id: quest id
    :return: True if tags are loaded
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        for tag in tags:
            cursor.execute('SELECT tag_id FROM tag WHERE tag_name = %s', (tag,))
            tag_id = cursor.fetchone()
            if tag_id is None:
                print("Creating new tag")
                cursor.execute('INSERT INTO tag (tag_name) '
                               'VALUES (%s) RETURNING tag_id', (tag,))
                tag_id = cursor.fetchone()
            cursor.execute('INSERT INTO quest_tag (quest_id, tag_id) '
                           'VALUES (%s, %s)', (quest_id, tag_id['tag_id']))

    return True

def set_rating(quest_id, rating: dict):
    """
    Add row to table ratings
    :param quest_id: quest id
    :param rating: data to load
    :return: rating id
    """
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO rating (quest_id, one_star_amount, two_star_amount,'
                       'three_star_amount, four_star_amount, five_star_amount)'
                       'VALUES (%s, %s, %s, %s, %s, %s) RETURNING rating_id',
                       (quest_id, rating['one'], rating['two'],
                        rating['three'], rating['four'],
                        rating['five']))
        return cursor.fetchone()['rating_id']
    
def set_block(block, quest_id):
    with get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO block ( quest_id, block_text, block_type_id, pos_x, pos_y) '
                       'VALUES ( %s, %s, %s, %s, %s) RETURNING block_id',
                       (quest_id, block.block_text, block.block_type_id, block.position.x, block.position.y))
        block.db_id = cursor.fetchone()['block_id']
    return True

def set_blocks_link(source_id: int, target_id: int):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE block SET next_block_id = %s WHERE block_id = %s', (target_id, source_id))

def set_answer_and_block_link(answer_id: int, block_id: int):
    with get_db(), get_db().cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('UPDATE answer_option SET next_block_id = %s WHERE option_id = %s', (block_id, answer_id))

def get_block_media_id(block_id: int):
    """
    Return all media by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT media_id FROM block_media WHERE block_id = %s", (block_id, ))
        return cursor.fetchall()
    
def get_block_media(block_id: int):
    """
    Return all media by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT * FROM block_media WHERE block_id = %s", (block_id, ))
        return cursor.fetchone()
    
def get_block_answer_option_id(block_id: int):
    """
    Return all answers by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT option_id FROM answer_option WHERE block_id = %s", (block_id, ))
        return cursor.fetchall()
    
def get_answer_option(answer_id: int):
    """
    Return all answers by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT * FROM answer_option WHERE option_id = %s", (answer_id, ))
        return cursor.fetchone()
    
def get_block_place_id(block_id: int):
    """
    Return place id by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT place_id FROM place WHERE block_id = %s", (block_id, ))
        return cursor.fetchone()
    
def get_block_place(place_id: int):
    """
    Return place by place id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT * FROM place WHERE place_id = %s", (place_id, ))
        return cursor.fetchone()
    
def get_block_hint_id(block_id: int):
    """
    Return hint id by block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT hint_id FROM hint WHERE block_id = %s", (block_id, ))
        return cursor.fetchall()
    
def get_block_hint(hint_id: int):
    """
    Return hint by hint id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT * FROM hint WHERE hint_id = %s", (hint_id, ))
        return cursor.fetchone()
    
def get_hint_media_id(hint_id: int):
    """
    Return all media by hint id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT media_id FROM hint_media WHERE hint_id = %s", (hint_id, ))
        return cursor.fetchall()
    
def get_hint_media(hint_id: int):
    """
    Return media by hint id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT * FROM hint_media WHERE hint_id = %s", (hint_id, ))
        return cursor.fetchone()
    
def get_link(block_id: int):
    """
    Return next block by source block id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT next_block_id FROM block WHERE block_id = %s", (block_id, ))
        return cursor.fetchone()
    
def get_answer_link(answer_id: int):
    """
    Return next block by source answer id
    """
    with get_db().cursor() as cursor:
        cursor.execute("SELECT next_block_id FROM answer_option WHERE option_id = %s", (answer_id, ))
        return cursor.fetchone()