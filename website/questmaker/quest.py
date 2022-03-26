"""
Contains classes for database entities
"""

from . import db
from flask import g


class File:
    """
    File representation class
    """
    def __init__(self, f_type, url):
        """
        Create file object
        :param f_type: type of file (image, video, etc.)
        :param url: url for file resource
        """
        self.type = f_type
        self.url = url


class Hint:
    """
    Hint representation class
    """
    @staticmethod
    def from_db(hint_id):
        """
        Load hint from database
        :param hint_id: hint id in database
        :return: hint object with info from db
        """
        hint_info = db.get_hint(hint_id)
        hint = Hint(hint_info['hint_text'], hint_info['fine'])
        hint.files = [File(file['f_type_name'], file['url_for_file']) for file in db.get_hint_files(hint_id)]
        return hint

    def __init__(self, text=None, fine=0):
        """
        Create hint
        :param text: hint text
        :param fine: hint fine
        """
        self.text = text
        self.fine = fine


class Answer:
    """
    Answer (answer option in database) representation class
    """
    @staticmethod
    def from_db(answer_id):
        """
        Load answer from database
        :param answer_id: answer id in database
        :return: answer object with info from database
        """
        answer_info = db.get_answer_option(answer_id)
        answer = Answer(answer_info['option_text'], answer_info['points'])
        next_question_id = answer_info['next_question_id']
        if 'questions' in g and next_question_id in g.qustions.keys():
            # question has already been created
            answer.next_question = g.questions[next_question_id]
        else:
            answer.next_question = Question.from_db(next_question_id)
        return answer

    def __init__(self, text=None, points=0):
        """
        Create answer object
        :param text: answer text
        :param points: answer points
        """
        self.text = text
        self.points = points
        self.next_question = None


class Place:
    """
    Place representation class
    """
    @staticmethod
    def from_db(place_id):
        """
        Load place from database
        :param place_id: place id in database
        :return: place object with info from database
        """
        place = db.get_place(place_id)
        return Place(place['coords'], place['radius'], place['time_open'], place['time_close'])

    def __init__(self, coords=None, radius=None, time_open=None, time_close=None):
        """
        Create place object
        :param coords: place coordinates
        :param radius: radius where user is detected
        :param time_open: the earliest time user can visit place
        :param time_close: the latest time  user can visit place
        """
        self.coords = coords
        self.radius = radius
        self.time_open = time_open
        self.time_close = time_close


class Movement:
    """
    Movement representation class
    """
    @staticmethod
    def from_db(movement_id):
        """
        Load movement from database
        :param movement_id: movement id in database
        :return: movement object with info from database
        """
        move_info = db.get_movement(movement_id)
        move = Movement()
        move.place = Place.from_db(move_info['place_id'])
        next_question_id = move_info['next_question_id']
        if 'questions' in g and next_question_id in g.qustions.keys():
            # question has already been created
            move.next_question = g.qustions[next_question_id]
        else:
            move.next_question = Question.from_db(next_question_id)
        return move

    def __init__(self):
        self.place = None
        self.next_question = None


class Question:
    @staticmethod
    def from_db(question_id):
        """
        Load question from database
        :param question_id: question id in database
        :return: question object with info from database
        """
        question_info = db.get_question(question_id)
        question = Question()
        question.text = question_info['question_text']
        question.type = question_info['q_type_name']
        question.files = [File(file['f_type_name'], file['url_for_file'])
                          for file in db.get_question_files(question_id)]
        question.hints = [Hint().from_db(hint['hint_id']) for hint in db.get_question_hints_ids(question_id)]
        if question.type != 'end':
            question.answers = [Answer().from_db(answer['option_id'])
                                for answer in db.get_question_answer_options_ids(question_id)]
            question.movements = [Movement().from_db(move['movement_id'])
                                  for move in db.get_question_movements_ids(question_id)]
        if 'questions' not in g:
            g.questions = {}  # save mapped questions to process loops
        g.questions[question_id] = question  # save ref to question to avoid loop creating
        return question

    def __init__(self):
        self.type = None
        self.text = None
        self.hints = []
        self.files = []
        self.answers = []
        self.movements = []


class Quest:

    @staticmethod
    def from_db(quest_id):
        """
        Recursively load quest and related objects from database
        :param quest_id: quest id in database
        :return: quest object with info from database
        """
        g.questions = {}  # save mapped questions to process loops
        quest_info = db.get_quest(quest_id)
        quest = Quest()
        quest.title = quest_info['title']
        quest.author = quest_info['author']
        quest.description = quest_info['description']
        quest.password = quest_info['password']
        quest.time_open = quest_info['time_open']
        quest.time_close = quest_info['time_close']
        quest.lead_time = quest_info['lead_time']
        quest.cover_url = quest_info['cover_url']
        quest.hidden = quest_info['hidden']
        quest.tags = [tag['tag_name'] for tag in db.get_quest_tags(quest_id)]
        quest.files = [File(file['f_type_name'], file['url_for_file']) for file in db.get_quest_files(quest_id)]
        quest.first_question = Question().from_db(db.get_start_question_id(quest_id)['question_id'])
        quest.rating = db.get_quest_rating(quest_id)
        return quest

    def __init__(self):
        self.title = None
        self.author = None
        self.tags = []
        self.files = []
        self.hidden = False
        self.description = None
        self.password = None
        self.time_open = None
        self.time_close = None
        self.lead_time = None
        self.cover_url = None
        self.first_question = None
        self.rating = {'one': 0, 'two': 0, 'three': 0, 'four': 0, 'five': 0}

    def to_db(self):
        """
        Write quest to database
        """
        pass
