"""
Contains classes for database entities
"""

from . import db
from flask import g

from .db import set_author, set_quest, set_tags, set_quest_files, set_questions, \
    create_new_question

from .bfs import BFS


def update_from_dict(entity, entity_dict):
    """
    Change or add field from dictionary to quest entity
    :param entity: entity to change
    :param entity_dict: dictionary with new params
    """
    for key, value in entity_dict.items():
        if key in entity.__dict__.keys():
            entity.__setattr__(key, value)


class File:
    """
    File representation class
    """

    def __init__(self, f_type=None, url=None, parent=None):
        """
        Create file object
        :param f_type: type of file (image, video, etc.)
        :param url: url for file resource
        """
        self.type = f_type
        self.url = url
        self.parent = parent

    def to_dict(self):
        """
        Transform file to dictionary (thus to JSON) representation
        """
        return {'f_type': self.type, 'url_for_file': self.url}


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
        for file in hint.files:
            file.parent = hint
        return hint

    def __init__(self, text=None, fine=0, parent=None):
        """
        Create hint
        :param text: hint text
        :param fine: hint fine
        """
        self.text = text
        self.fine = fine
        self.files = []
        self.parent = parent

    def to_dict(self):
        """
        Transform hint to dictionary (thus to JSON) representation
        """
        return {'hint_text': self.text, 'fine': self.fine, 'files': [file.to_dict() for file in self.files]}


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
        """
        Transform answer to dictionary (thus to JSON) representation
        """
        return {'answer_option_id': self.answer_option_id,
                'text': self.text,
                'points': self.points,
                'next_question_id': self.next_question.question_id if self.next_question is not None else None}


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

    def __init__(self, coords=None, radius=None, time_open=None, time_close=None, parent=None):
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
        self.parent = parent

    def to_dict(self):
        """
        Transform place to dictionary (thus to JSON) representation
        """
        return {'coords': self.coords, 'radius': self.radius,
                'time_open': self.time_open, 'time_close': self.time_close}


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
        """
        Transform movement to dictionary (thus to JSON) representation
        """
        return {'movement_id': self.movement_id,
                'place': self.place.to_dict(),
                'next_question_id': self.next_question.question_id if self.next_question is not None else None}


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
        question.question_id = question_id
        question.text = question_info['question_text']
        question.type = question_info['q_type_name']

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

        if 'questions' not in g:
            g.questions = {}  # save mapped questions to process loops
        g.questions[question_id] = question  # save ref to question to avoid loop creating
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

    def to_dict(self):
        """
        Transform question to dictionary (thus to JSON) representation
        """
        return {'question_id': self.question_id, 'type': self.type, 'text': self.text,
                'files': [file.to_dict() for file in self.files],
                'hints': [hint.to_dict() for hint in self.hints],
                'answer_options': [ans.to_dict() for ans in self.answers],
                'movements': [move.to_dict() for move in self.movements]}


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
        quest.quest_id = quest_id
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
        for file in quest.files:
            file.parent = quest
        quest.first_question = Question().from_db(db.get_start_question_id(quest_id)['question_id'])
        quest.first_question.parents.append(quest)
        quest.rating = db.get_quest_rating(quest_id)
        return quest

    def __init__(self):
        self.quest_id = None
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

    def to_db(self, author: Author):
        """
        Write data from Quest object to database
        """
        quest_id = set_quest(self, author.email)
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
        """
        Transform quest to dictionary (thus to JSON) representation
        """
        quest_dict = {key: val for key, val in self.__dict__.items()
                      if key not in ['files', 'first_question', 'rating']}

        quest_dict['lead_time'] = quest_dict['lead_time'].total_seconds()
        quest_dict['start_question_id'] = self.first_question.question_id
        quest_dict['files'] = [file.to_dict() for file in self.files]
        quest_dict['questions'] = []
        for question in BFS(self.first_question):
            quest_dict['questions'].append(question.to_dict())

        return quest_dict

    def create_from_dict(self, quest_dict):
        """
        Create new quest using params from dictionary
        :param quest_dict: dictionary with quest params
        """
        update_from_dict(self, quest_dict)
        startQuestion = Question()
        startQuestion.type = 'start'
        startQuestion.answers.append(Answer())
        self.first_question = startQuestion
