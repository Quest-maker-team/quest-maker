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

