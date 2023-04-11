import psycopg2
from psycopg2.extras import DictCursor
import datetime
import os


class MetaSingleton(type):
    """
    A metaclass for implementing the singleton pattern
    """
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__()
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    """
    The type to communicate with the database (is a singleton)
    """
    connection = None

    def connect(self):
        """
        Create new database connection or use current if exists
        :param self: instance
        :return: connection object
        """
        if self.connection is None:      
            name = os.environ['DB_NAME']
            user = os.environ['DB_USER']
            password = os.environ['DB_PASSWORD']
            host = os.environ['DB_HOST']
            port = os.environ['DB_PORT']
            self.connection = psycopg2.connect(dbname=name, user=user, password=password, host=host, port=port)
        return self.connection

    def __del__(self):
        """
        Close database connection if exists
        :param self: instance
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None


def select_one(query, params):
    """
    Executes the received selection request with the received parameters.
    :param query: selection request
    :param params: request parameters
    :return: matching row from table
    :return: None if there are no matching rows
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            res = cursor.fetchone()

    return res


def select_all(query, params):
    """
    Executes the received selection request with the received parameters.
    :param query: selection request
    :param params: request parameters
    :return: all matching rows from table
    :return: empty list if there are no matching rows
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            res = cursor.fetchall()

    return res


def insert_or_update(query, params):
    """
    Executes the received insert or update request with the received parameters.
    :param query: selection request
    :param params: request parameters
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            conn.commit()


def get_quest_title(quest_keyword):
    """
    Find active quest title in table quest by id
    :param quest_keyword: quest keyword
    :return: tuple (id, name) of the quest with the specified keyword
    :return: None if quest with the same id don't exist
    """
    try:
        info = select_one('SELECT quest_id, title, time_open, time_close, periodicity FROM quest WHERE keyword= %s'
                          ' AND hidden= %s AND published= %s', (quest_keyword, 'false', 'true',))
        if info:
            now = datetime.datetime.now().astimezone()
            open = True
            not_close = True
            if info[3] != None:
                if now > info[3] and info[2] != None and info[4] != None:
                    k = int((now - info[2]) / info[4])
                    now = now - k * info[4]
                not_close = now < info[3]
            if info[2] != None:
                open = now > info[2]
            if open and not_close:
                return info[0], info[1]
            else:
                return None
        else:
            return None
    except:
        #In case a non-integer is entered
        return None


def get_private_quest_title(quest_keyword):
    """
    Find published private quest title in table quest by id
    :param quest_keyword: quest keyword
    :return: tuple (id, name, password) of the quest with the specified keyword
    :return: None if quest with the same id don't exist
    """
    try:
        info = select_one('SELECT quest_id, title, time_open, time_close, periodicity, password'
                          ' FROM quest WHERE keyword= %s AND hidden= %s AND published= %s AND password IS NOT NULL',
                          (quest_keyword, 'false', 'true',))
        if info:
            now = datetime.datetime.now().astimezone()
            open = True
            not_close = True
            if info[3] != None:
                if now > info[3] and info[2] != None and info[4] != None:
                    k = int((now - info[2]) / info[4])
                    now = now - k * info[4]
                not_close = now < info[3]
            if info[2] != None:
                open = now > info[2]
            if open and not_close:
                return info[0], info[1], info[5]
            else:
                return None
        else:
            return None
    except:
        #In case a non-integer is entered
        return None


def get_quest_time_info(quest_id):
    """
    Find quest time limits in table quest by id
    :param quest_id: quest id
    :return: time_close and lead_time
    :return: None if quest with the same id don't exist
    """
    try:
        return select_one('SELECT time_close, lead_time FROM quest WHERE quest_id= %s', (quest_id, ))
    except:
        #In case a non-integer is entered
        return None


def get_block_by_id(block_id):
    """
    Find block in table block by id
    :param block_id: block id
    :return: block id, block text, block type name and next block id tuple
    :return: None if block with the same id don't exist
    """
    try:
        return select_one('SELECT block_id, block_text, block_type_name, next_block_id FROM block INNER JOIN block_type'
                          ' ON block.block_type_id= block_type.block_type_id WHERE block_id= %s', (block_id, ))
    except:
        #In case a non-integer is entered
        return None


def get_start_block(quest_id):
    """
    Find first block related to the quest
    :param quest_id: quest id
    :return: first block id, block text and next block id tuple
    :return: None in case of failure
    """
    try:
        return select_one('SELECT block_id, block_text, next_block_id FROM block INNER JOIN block_type '
                            'ON block.block_type_id= block_type.block_type_id WHERE quest_id= %s '
                            'AND block_type_name= %s', (quest_id, 'start_block', ))
    except:
        return None


def get_answer_options(question_id):
    """
    Find answer options related to the question
    :param question_id: question id
    :return: a list of tuples with values option_text, points, next_block_id
    :return: None in case of failure
    """
    try:
        return select_all('SELECT option_text, points, next_block_id FROM answer_option WHERE block_id= %s',
                          (question_id, ))
    except:
        return None


def get_place(movement_id):
    """
    Find place related to the movement
    :param movement_id: movement id
    :return: tuple with values latitude, longitude, radius, time_open, time_close
    :return: None in case of failure
    """
    try:
        return select_one('SELECT latitude, longitude, radius, time_open, time_close FROM place'
                          ' WHERE block_id= %s', (movement_id, ))
    except:
        return None


def get_hints(block_id):
    """
    Find all hints related to the block
    :param block_id: block id
    :return: a list of tuples with values hint_id, fine, hint_text
    :return: None in case of failure
    """
    try:
        return select_all('SELECT hint_id, fine, hint_text FROM hint WHERE block_id= %s', (block_id, ))
    except:
        return None


def get_hint_files(hint_id):
    """
    Find all files related to the hint
    :param hint_id: hint id
    :return: list of tuples with values media_path, media_type_name
    :return: None in case of failure
    """
    try:
        return select_all('SELECT media_path, media_type_name FROM hint_media INNER JOIN media_type '
                          'ON hint_media.media_type_id= media_type.media_type_id WHERE hint_id= %s', (hint_id, ))
    except:
        return None


def get_block_files(block_id):
    """
    Find all files related to the block
    :param block_id: block id
    :return: list of tuples with values media_path, media_type_name
    :return: None in case of failure
    """
    try:
        return select_all('SELECT media_path, media_type_name FROM block_media INNER JOIN media_type '
                          'ON block_media.media_type_id= media_type.media_type_id WHERE block_id= %s', (block_id, ))
    except:
        return None


def save_history(quest_id, telegram_id, is_finished, last_block_id, final_score, start_time, complition_time):
    """
    Add an entry with the passed values to the histories table
    :param quest_id: quest id
    :param telegram_id: user id
    :param is_finished: quest status, is true if it is completed to the end
    :param last_block_id: id of the block where user left off, can be None if the resumption is not expected
    :param final_score: final score 
    :param start_time: start time of the quest by the player
    :param complition_time: time spent completing the quest
    """
    try:
        history_id = select_one('SELECT history_id FROM history WHERE quest_id= %s AND telegram_id= %s',
                                (quest_id, telegram_id, ))
        if history_id is None:
            insert_or_update('INSERT INTO history (quest_id, telegram_id, is_finished, last_block_id, final_score, '
                             'start_time, complition_time) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                             (quest_id, telegram_id, is_finished, last_block_id, final_score, start_time, complition_time, ))
        else:
            insert_or_update('UPDATE history SET is_finished= %s, last_block_id= %s, final_score= %s, '
                             'complition_time= %s WHERE history_id= %s',
                             (is_finished, last_block_id, final_score, complition_time, history_id[0], ))
    except:
        pass


def get_history(quest_id, telegram_id):
    """
    Find data in the histories table for the specified quest and user
    :param quest_id: quest id
    :param telegram_id: user id
    :return: tuple with values is_finished, last_block_id, final_score, complition_time
    :return: None in case of failure
    """
    try:
        return select_one('SELECT is_finished, last_block_id, final_score, complition_time FROM history '
                          'WHERE quest_id= %s AND telegram_id= %s', (quest_id, telegram_id, ))
    except:
        return None


def update_rating(quest_id, rating):
    """
    Update rating
    :param quest_id: quest id
    :param rating: rating - 1, 2, 3, 4 or 5
    """
    table_column_names = {
        1: 'one_star_amount',
        2: 'two_star_amount',
        3: 'three_star_amount',
        4: 'four_star_amount',
        5: 'five_star_amount',
    }
    if rating not in table_column_names:
        return
    try:
        rating_id = select_one('SELECT rating_id FROM rating WHERE quest_id= %s',
                                (quest_id, ))
        if rating_id == None:
            insert_or_update('INSERT INTO rating (quest_id, %s) VALUES (%s, %s)', 
                             (table_column_names[rating], quest_id, 1, ))
        else:
            insert_or_update('UPDATE rating SET %s = %s + 1 WHERE rating_id = %s',
                         (table_column_names[rating], table_column_names[rating], rating_id[0], ))
    except:
        pass