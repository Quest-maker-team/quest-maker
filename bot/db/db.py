from configparser import ConfigParser
import psycopg2
from psycopg2.extras import DictCursor


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

    def close(self):
        """
        Close database connection if exists
        :param self: instance
        """
        if self.connection is not None:
            self.connection.close()


def select_one(query, params):
    """
    Executes the received selection request with the received parameters.
    :param query: selection request
    :param params: request parameters
    :return: matching row from table
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            res = cursor.fetchone()
            if not res:
                return False

    return res


def select_all(query, params):
    """
    Executes the received selection request with the received parameters.
    :param query: selection request
    :param params: request parameters
    :return: all matching rows from table
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            res = cursor.fetchall()
            if not res:
                return False

    return res


def get_quest_by_id(quest_id):
    """
    Find quest in table quest by id
    :param quest_id: quest id
    :return: matching row from table quest
    """
    return select_one('SELECT * FROM quest WHERE id= %s', (quest_id, ))


def get_files(object_id, type):
    """
    Finds all files related to the object
    :param object_id: object id
    :param type: type of object such as 'quest', 'place' etc.
    :return: all matching rows from table files
    """
    object_type_id = select_one("SELECT id FROM object_type WHERE type= %s", (type, ))[0]
    if not object_type_id:
        return False

    return select_all('SELECT url_for_file, type_of_file FROM files '
                      'WHERE id= %s AND type_of_object_id= %s ORDER BY id', (object_id, object_type_id, ))


def get_place_by_id(place_id):
    """
    Find place in table place by id
    :param place_id: place id
    :return: matching row from table place
    """
    return select_one('SELECT * FROM place WHERE id= %s', (place_id, ))


def get_directions(place_id):
    """
    Find all directions from received place
    :param place_id: place id
    :return: all matching rows from table directions
    """
    return select_all('SELECT next_place_id, description FROM directions WHERE cur_place_id= %s', (place_id, ))


def get_questions(place_id):
    """
    Find all questions related to the place
    :param place_id: place id
    :return: all matching rows from table question
    """
    return select_all('SELECT * FROM question WHERE place_id= %s ORDER BY id', (place_id, ))


def get_answer(question_id):
    """
    Find answer related to the question
    :param question_id: question id
    :return: all matching rows from table answer
    """
    return select_all('SELECT id, answer_text FROM answer WHERE question_id= %s', (question_id, ))


def get_possible_answers(question_id):
    """
    Find all possible answers related to the question
    :param question_id: question id
    :return: all matching rows from table possible_answer
    """
    return select_all('SELECT id, possible_ans_text FROM possible_answer WHERE question_id= %s', (question_id, ))


def get_hints(question_id):
    """
    Find all hints related to the question
    :param question_id: question id
    :return: all matching rows from table hints
    """
    return select_all('SELECT id, hint_text, fine FROM hints WHERE question_id= %s', (question_id, ))


def check_user_history(user_id, quest_id):
    """
    Checks if the given quest has been interrupted
    :param user_id: user id
    :param quest_id: quest id
    :return: matching row from table history or false if quest was complited
    """
    return select_one('SELECT last_place_id, final_score FROM history WHERE user_id= %s AND '
                      'quest_id= %s AND is_finished= false', (user_id, quest_id, ))