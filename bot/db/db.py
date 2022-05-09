from configparser import ConfigParser
from nis import match
import psycopg2
from psycopg2.extras import DictCursor
import datetime


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
            config = ConfigParser()
            config.read('db_config.ini')
            name = config['DB']['NAME']
            user = config['DB']['USER']
            password = config['DB']['PASSWORD']
            host = config['DB']['HOST']
            port = config['DB']['PORT']
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
        info = select_one("SELECT quest_id, title, time_open, time_close FROM quests WHERE keyword= %s AND hidden= %s",
                          (quest_keyword, 'false',))
        if info:
            now = datetime.datetime.now()
            open = True
            not_close = True
            if info[2] != None:
                open = now > info[2]
            if info[3] != None:
                not_close = now < info[3]
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
        info = select_one("SELECT quest_id, title, time_open, time_close, password"
                          " FROM quests WHERE keyword= %s AND published= %s AND password IS NOT NULL",
                          (quest_keyword, 'true',))
        if info:
            now = datetime.datetime.now()
            open = True
            not_close = True
            if info[2] != None:
                open = now > info[2]
            if info[3] != None:
                not_close = now < info[3]
            if open and not_close:
                return info[0], info[1], info[4]
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
        return select_one("SELECT time_close, lead_time FROM quests WHERE quest_id= %s", (quest_id, ))
    except:
        #In case a non-integer is entered
        return None


def get_question_by_id(question_id):
    """
    Find question in table questions by id
    :param question_id: question id
    :return: question id, question text and question type name tuple
    :return: None if question with the same id don't exist
    """
    try:
        return select_one('SELECT question_id, question_text, q_type_name FROM questions INNER JOIN question_types '
                          'ON questions.q_type_id= question_types.q_type_id WHERE question_id= %s', (question_id, ))
    except:
        #In case a non-integer is entered
        return None


def get_first_question(quest_id):
    """
    Find first question related to the quest
    :param quest_id: quest id
    :return: greeting message and first question id, question text and question type name tuple
    :return: ('', None) in case of failure
    """
    try:
        bogus_question = select_one('SELECT question_id, question_text FROM questions INNER JOIN question_types '
                                    'ON questions.q_type_id= question_types.q_type_id WHERE quest_id= %s '
                                    'AND q_type_name= %s', (quest_id, 'start', ))
        real_question_id = select_one('SELECT next_question_id FROM answer_options WHERE question_id= %s',
                                      (bogus_question[0], ))[0]
        return (bogus_question[1], get_question_by_id(real_question_id))
    except:
        return ('', None)


def get_answer_options(question_id):
    """
    Find answer options related to the question
    :param question_id: question id
    :return: a list of tuples with values option_text, points, next_question_id
    :return: None in case of failure
    """
    try:
        return select_all('SELECT option_text, points, next_question_id FROM answer_options WHERE question_id= %s',
                          (question_id, ))
    except:
        return None


def get_movement(question_id):
    """
    Find movement related to the question
    :param question_id: question id
    :return: tuple with values next_question_id, coords, radius, time_open, time_close
    :return: None in case of failure
    """
    try:
        return select_one('SELECT next_question_id, coords, radius, time_open, time_close FROM movements '
                          'INNER JOIN places ON movements.place_id= places.place_id WHERE question_id= %s',
                          (question_id, ))
    except:
        return None


def get_hints(question_id):
    """
    Find all hints related to the question
    :param question_id: question id
    :return: a list of tuples with values hint_id, fine, hint_text
    :return: None in case of failure
    """
    try:
        return select_all('SELECT hint_id, fine, hint_text FROM hints WHERE question_id= %s', (question_id, ))
    except:
        return None


def get_hint_files(hint_id):
    """
    Find all files related to the hint
    :param hint_id: hint id
    :return: list of tuples with values url_for_file, f_type_name
    :return: None in case of failure
    """
    try:
        return select_all('SELECT url_for_file, f_type_name FROM hint_files INNER JOIN files '
                          'ON hint_files.f_id= files.f_id INNER JOIN file_types '
                          'ON files.f_type_id= file_types.f_type_id WHERE hint_id= %s', (hint_id, ))
    except:
        return None


def get_question_files(question_id):
    """
    Find all files related to the question
    :param question_id: question id
    :return: list of tuples with values url_for_file, f_type_name
    :return: None in case of failure
    """
    try:
        return select_all('SELECT url_for_file, f_type_name FROM question_files INNER JOIN files '
                          'ON question_files.f_id= files.f_id INNER JOIN file_types '
                          'ON files.f_type_id= file_types.f_type_id WHERE question_id= %s', (question_id, ))
    except:
        return None


def save_history(quest_id, telegram_id, is_finished, last_question_id, final_score):
    """
    Add an entry with the passed values to the histories table
    :param quest_id: quest id
    :param telegram_id: user id
    :param is_finished: quest status, is true if it is completed to the end
    :param last_question_id: id of the question where user left off, can be None if the resumption is not expected
    :param final_score: final score 
    """
    try:
        history_id = select_one('SELECT history_id FROM histories WHERE quest_id= %s AND telegram_id= %s',
                                (quest_id, telegram_id, ))
        if history_id is None:
            insert_or_update('INSERT INTO histories (quest_id, telegram_id, is_finished, last_question_id, '
                             'final_score) VALUES (%s, %s, %s, %s, %s)', 
                             (quest_id, telegram_id, is_finished, last_question_id, final_score, ))
        else:
            insert_or_update('UPDATE histories SET is_finished= %s, last_question_id= %s, final_score= %s '
                             'WHERE history_id= %s', (is_finished, last_question_id, final_score, history_id[0], ))
    except:
        pass


def get_history(quest_id, telegram_id):
    """
    Find data in the histories table for the specified quest and user
    :param quest_id: quest id
    :param telegram_id: user id
    :return: tuple with values is_finished, last_question_id, final_score
    :return: None in case of failure
    """
    try:
        return select_one('SELECT is_finished, last_question_id, final_score FROM histories '
                          'WHERE quest_id= %s AND telegram_id= %s', (quest_id, telegram_id, ))
    except:
        return None


def update_rating(quest_id, rating):
    """
    Update rating
    :param quest_id: quest id
    :param rating: rating - 1, 2, 3, 4 or 5
    :return: true if success, false - otherwise
    """
    query = "UPDATE ratings SET {0} = {0} + 1 WHERE quest_id = {1}"
    table_column_names = {
        1: "one_star_amount",
        2: "two_star_amount",
        3: "three_star_amount",
        4: "four_star_amount",
        5: "five_star_amount",
    }
    if rating not in table_column_names:
        return False
    try:
        with Database().connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query.format(table_column_names[rating], quest_id))
                conn.commit()
        return True
    except:
        return False
