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
    :return: None if there are no matching rows
    """
    with Database().connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query, params)
            res = cursor.fetchall()

    return res


def get_quest_title(quest_id):
    """
    Find quest title in table quest by id
    :param quest_id: quest id
    :return: name of the quest with the specified id
    :return: None if quest with the same id don't exist
    """
    try:
        name = select_one("SELECT title FROM quests WHERE quest_id= %s", (quest_id, ))
        if name:
            return name[0]
        else:
            return None
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
    :return: first question id, question text and question type name tuple
    :return: None in case of failure
    """
    try:
        bogus_question_id = select_one('SELECT question_id FROM questions INNER JOIN question_types '
                                       'ON questions.q_type_id= question_types.q_type_id WHERE quest_id= %s '
                                       'AND q_type_name= %s', (quest_id, 'start', ))[0]
        real_question_id = select_one('SELECT next_question_id FROM answer_options WHERE question_id= %s',
                                      (bogus_question_id, ))[0]
        return get_question_by_id(real_question_id)
    except:
        return None


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
    :return: tuple with values next_question_id, coords, radius
    :return: None in case of failure
    """
    try:
        return select_one('SELECT next_question_id, coords, radius FROM movements INNER JOIN places '
                          'ON movements.place_id= places.place_id WHERE question_id= %s', (question_id, ))
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


if __name__ == '__main__':
    info = get_question_files(6)
    print(info)