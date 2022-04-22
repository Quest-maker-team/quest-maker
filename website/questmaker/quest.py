"""
Contains classes for database entities
"""

from . import db
from .db import set_author, set_quest, set_tags, set_quest_files, set_questions, \
    create_new_question
from .bfs import BFS

from flask import g
from abc import ABC, abstractmethod


def update_from_dict(entity, entity_dict):
    """
    Change or add field from dictionary to quest entity
    :param entity: entity to change
    :param entity_dict: dictionary with new params
    :return: True if success else False
    """
    for attr, value in entity_dict.items():
        if type(entity).check_valid_update_attr(attr, value):
            entity.__setattr__(attr, value)
        else:
            return False
    return True


class QuestEntity(ABC):
    """
    Common class for all quest entities
    """

    @abstractmethod
    def to_dict(self):
        """
        Transform entity to dictionary (thus to JSON) representation
        """
        pass

    @abstractmethod
    def remove_from_graph(self):
        """
        Remove entity from quest graph and clear all related links (graph can become disconnected)
        """
        pass

    @staticmethod
    @abstractmethod
    def check_valid_update_attr(attr, val):
        """
        Check possibility to assign value to attribute
        """
        pass

    @staticmethod
    @abstractmethod
    def check_creation_attrs(attrs):
        """
        Check that list attrs contains necessary attributes to create new entity
        """
        pass


class File(QuestEntity):
    """
    File representation class
    """

    def __init__(self, f_type=None, url=None, parent=None):
        """
        Create file object
        :param f_type: type of file (image, video, etc.)
        :param url: url for file resource
        """
        self.file_id = None
        self.type = f_type
        self.url = url
        self.parent = parent

    def to_dict(self):
        return {'file_d': self.file_id, 'f_type': self.type, 'url_for_file': self.url}

    def remove_from_graph(self):
        if self.parent and self in self.parent.files:
            self.parent.files.remove(self)
            self.parent = None

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr == 'type':
            return val in db.get_file_types()
        elif attr == 'url':
            return isinstance(val, str)
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['type', 'url']])


class Author:
    def __init__(self, name, password, email, status, avatar_url):
        self.name = name
        self.password = password
        self.email = email
        self.status = status
        self.avatar_url = avatar_url

    def to_db(self):
        author_id = set_author(self)
        return author_id


class Hint(QuestEntity):
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
        for file in hint.files:
            file.parent = hint
        return hint

    def __init__(self, text=None, fine=0, parent=None):
        """
        Create hint
        :param text: hint text
        :param fine: hint fine
        """
        self.hint_id = None
        self.text = text
        self.fine = fine
        self.files = []
        self.parent = parent

    def to_dict(self):
        return {'hint_id': self.hint_id, 'hint_text': self.text, 'fine': self.fine,
                'files': [file.to_dict() for file in self.files]}

    def remove_from_graph(self):
        self.files = []
        if self.parent and self in self.parent.hints:
            self.parent.hints.remove(self)
        self.parent = None

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr == 'text':
            return isinstance(val, str)
        if attr == 'fine':
            return isinstance(val, (int, float))
        return True

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['text']])


class Answer(QuestEntity):
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
        answer.answer_option_id = answer_id
        next_question_id = answer_info['next_question_id']
        if 'questions' in g and next_question_id in g.questions.keys():
            # question has already been created
            answer.next_question = g.questions[next_question_id]
        else:
            answer.next_question = Question.from_db(next_question_id)
        answer.next_question.parents.append(answer)

        return answer

    def __init__(self, text=None, points=0, parent=None):
        """
        Create answer object
        :param text: answer text
        :param points: answer points
        """
        self.answer_option_id = None
        self.text = text
        self.points = points
        self.next_question = None
        self.parent = parent

    def to_dict(self):
        return {'answer_option_id': self.answer_option_id,
                'text': self.text,
                'points': self.points,
                'next_question_id': self.next_question.question_id if self.next_question is not None else None}

    def remove_from_graph(self):
        if self.next_question and self in self.next_question.parents:
            self.next_question.parents.remove(self)
        if self.parent and self in self.parent.answers:
            self.parent.answers.remove(self)
        self.next_question = None
        self.parent = None

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr == 'points':
            return isinstance(val, (int, float))
        elif attr == 'text':
            return isinstance(val, str)
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['text']])


class Place(QuestEntity):
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

    def __init__(self, coords=None, radius=None, time_open=None, time_close=None, parent=None):
        """
        Create place object
        :param coords: place coordinates
        :param radius: radius where user is detected
        :param time_open: the earliest time user can visit place
        :param time_close: the latest time  user can visit place
        """
        self.place_id = None
        self.coords = coords
        self.radius = radius
        self.time_open = time_open
        self.time_close = time_close
        self.parent = parent

    def to_dict(self):
        return {'place_id': self.place_id, 'coords': self.coords, 'radius': self.radius,
                'time_open': self.time_open, 'time_close': self.time_close}

    def remove_from_graph(self):
        if self.parent:
            self.parent.place = None
        self.parent = None

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr == 'coords':
            return isinstance(val, list) and len(val) == 2 and isinstance(val[0], float) and isinstance(val[1], float)
        elif attr == 'radius':
            return isinstance(val, (int, float))
        elif attr == 'time_open' or attr == 'time_close':
            # TODO: add time support
            return False
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['coords', 'radius']])


class Movement(QuestEntity):
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
        move.movement_id = movement_id
        move.place = Place.from_db(move_info['place_id'])
        move.place.parent = move

        next_question_id = move_info['next_question_id']
        if 'questions' in g and next_question_id in g.questions.keys():
            # question has already been created
            move.next_question = g.questions[next_question_id]
        else:
            move.next_question = Question.from_db(next_question_id)

        move.next_question.parents.append(move)
        return move

    def __init__(self, parent=None):
        self.movement_id = None
        self.place = None
        self.next_question = None
        self.parent = parent

    def to_dict(self):
        return {'movement_id': self.movement_id,
                'place': self.place.to_dict() if self.place else None,
                'next_question_id': self.next_question.question_id if self.next_question is not None else None}

    def remove_from_graph(self):
        if self.next_question and self in self.next_question.parents:
            self.next_question.parents.remove(self)
        if self.parent and self in self.parent.movements:
            self.parent.movements.remove(self)
        self.place = None
        self.next_question = None
        self.parent = None

    @staticmethod
    def check_valid_update_attr(attr, val):
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return not attrs


class Question(QuestEntity):
    @staticmethod
    def from_db(question_id):
        """
        Load question from database
        :param question_id: question id in database
        :return: question object with info from database
        """
        question_info = db.get_question(question_id)
        question = Question()
        if 'questions' not in g:
            g.questions = {}  # save mapped questions to process loops
        g.questions[question_id] = question  # save ref to question to avoid loop creating
        question.question_id = question_id
        question.text = question_info['question_text']
        question.type = question_info['q_type_name']
        question.pos_x = question_info['pos_x']
        question.pos_y = question_info['pos_y']

        question.files = [File(file['f_type_name'], file['url_for_file'], question)
                          for file in db.get_question_files(question_id)]

        for file in question.files:
            file.parent = question

        question.hints = [Hint().from_db(hint['hint_id']) for hint in db.get_question_hints_ids(question_id)]
        for hint in question.hints:
            hint.parent = question

        if question.type != 'end':
            question.answers = [Answer().from_db(answer['option_id'])
                                for answer in db.get_question_answer_options_ids(question_id)]
            question.movements = [Movement().from_db(move['movement_id'])
                                  for move in db.get_question_movements_ids(question_id)]
            for ans in question.answers:
                ans.parent = question
            for move in question.movements:
                move.parent = question

        return question

    def __init__(self):
        self.question_id = None
        self.type = None
        self.text = None
        self.hints = []
        self.files = []
        self.answers = []
        self.movements = []
        self.parents = []
        self.pos_x = 0
        self.pos_y = 0

    def to_dict(self):
        return {'question_id': self.question_id, 'type': self.type, 'text': self.text,
                'files': [file.to_dict() for file in self.files],
                'hints': [hint.to_dict() for hint in self.hints],
                'answer_options': [ans.to_dict() for ans in self.answers],
                'movements': [move.to_dict() for move in self.movements],
                'pos_x': self.pos_x,
                'pos_y': self.pos_y}

    def remove_from_graph(self):
        for parent in self.parents:
            parent.next_question = None
        for answer in self.answers:
            answer.parent = None
        for move in self.movements:
            move.parent = None
        self.answers = []
        self.movements = []
        self.files = []
        self.hints = []
        self.parents = []

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr == 'type':
            return val in db.get_question_types()
        elif attr == 'pos_x' or attr == 'pos_y':
            return isinstance(val, int)
        elif attr == 'text':
            return isinstance(val, str)
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['type']])


class Quest(QuestEntity):
    @staticmethod
    def from_db(quest_id):
        """
        Recursively load quest and related objects from database
        :param quest_id: quest id in database
        :return: quest object with info from database
        """
        g.questions = {}  # save mapped questions to process loops
        quest_info = db.get_quest(quest_id)
        if not quest_info:
            return None
        quest = Quest()
        quest.id_in_db = quest_id
        quest.quest_id = quest_id
        quest.title = quest_info['title']
        quest.author_id = quest_info['author_id']
        quest.description = quest_info['description']
        quest.password = quest_info['password']
        quest.time_open = quest_info['time_open']
        quest.time_close = quest_info['time_close']
        quest.lead_time = quest_info['lead_time']
        quest.cover_url = quest_info['cover_url']
        quest.hidden = quest_info['hidden']
        quest.tags = [tag['tag_name'] for tag in db.get_quest_tags(quest_id)]
        quest.files = [File(file['f_type_name'], file['url_for_file']) for file in db.get_quest_files(quest_id)]
        for file in quest.files:
            file.parent = quest
        quest.first_question = Question().from_db(db.get_start_question_id(quest_id)['question_id'])
        quest.first_question.parents.append(quest)
        quest.rating = db.get_quest_rating(quest_id)
        return quest

    def __init__(self):
        self.id_in_db = None
        self.quest_id = None
        self.title = None
        self.author_id = None
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
        Write data from Quest object to database
        """
        quest_id = set_quest(self)
        set_tags(self, quest_id)
        question_id = create_new_question(self.first_question, quest_id)
        questions = dict()
        questions[self.first_question] = question_id
        used_files = set_quest_files(self.files, quest_id)
        if self.first_question.type != 'start':
            return False
        else:
            return set_questions(used_files, self.first_question, quest_id, {}, question_id, questions, {}, {})

    def to_dict(self):
        quest_dict = dict()
        quest_dict['quest_id'] = self.quest_id
        quest_dict['title'] = self.title
        quest_dict['tags'] = self.tags
        quest_dict['hidden'] = self.hidden
        quest_dict['description'] = self.description
        quest_dict['password'] = self.password
        quest_dict['time_open'] = self.time_open
        quest_dict['time_close'] = self.time_close
        if self.lead_time is not None:
            quest_dict['lead_time'] = self.lead_time.total_seconds()
        quest_dict['start_question_id'] = self.first_question.question_id
        quest_dict['files'] = [file.to_dict() for file in self.files]
        quest_dict['questions'] = []
        for question in BFS(self.first_question):
            quest_dict['questions'].append(question.to_dict())

        return quest_dict

    def remove_from_graph(self):
        pass

    @staticmethod
    def check_valid_update_attr(attr, val):
        if attr in ['title', 'description', 'password']:
            return isinstance(val, str)
        elif attr == 'hidden':
            return isinstance(val, bool)
        elif attr in ['time_open', 'time_close', 'lead_time']:
            # TODO: add time support
            return False
        return False

    @staticmethod
    def check_creation_attrs(attrs):
        return all([(attr in attrs) for attr in ['title']])

    def create_from_dict(self, quest_dict):
        """
        Create new quest using params from dictionary
        :param quest_dict: dictionary with quest params
        :return: True if success else False
        """
        if 'title' not in quest_dict.keys():
            return False
        rc = update_from_dict(self, quest_dict)
        if not rc:
            return False
        startQuestion = Question()
        startQuestion.type = 'start'
        startQuestion.answers.append(Answer())
        startQuestion.answers[0].parent = startQuestion
        endQuestion = Question()
        endQuestion.type = 'end'
        endQuestion.parent = startQuestion.answers[0]
        startQuestion.answers[0].next_question = endQuestion
        self.first_question = startQuestion
        return True
