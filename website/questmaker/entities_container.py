"""
Contains container class to store quest entities
"""

from .quest import Quest, Question, Answer, Movement, Hint, Place, File
from .bfs import BFS


class EntityType:
    """
    Enum class for quest entities types
    """
    QUEST = 0
    QUESTION = 1
    ANSWER = 2
    MOVEMENT = 3
    HINT = 4
    PLACE = 5
    FILE = 6
    __num_of_types = 7

    @classmethod
    def num_of_types(cls):
        """
        Number of quest entities
        """
        return cls.__num_of_types

    @classmethod
    def get_types(cls):
        return set(i for i in range(cls.__num_of_types))

    @classmethod
    def from_str(cls, e_type_str):
        """
        Get enum value from entity string name
        """
        if e_type_str == 'quest':
            return EntityType.QUEST
        elif e_type_str == 'question':
            return EntityType.QUESTION
        elif e_type_str == 'answer':
            return EntityType.ANSWER
        elif e_type_str == 'hint':
            return EntityType.HINT
        elif e_type_str == 'place':
            return EntityType.PLACE
        elif e_type_str == 'file':
            return EntityType.FILE
        elif e_type_str == 'movement':
            return EntityType.MOVEMENT
        else:
            return None

    @classmethod
    def from_instance(cls, entity):
        """
        Get enum value of entity instance
        """
        if isinstance(entity, Quest):
            return cls.QUEST
        elif isinstance(entity, Question):
            return cls.QUESTION
        elif isinstance(entity, Answer):
            return cls.ANSWER
        elif isinstance(entity, Hint):
            return cls.HINT
        elif isinstance(entity, Movement):
            return cls.MOVEMENT
        elif isinstance(entity, Place):
            return cls.PLACE
        elif isinstance(entity, File):
            return cls.FILE
        else:
            return None


class EntitiesContainer:
    """
    Class to store quest while it's created in constructor
    """
    def __init__(self):
        self.__cur_ids = {e_type: 0 for e_type in range(EntityType.num_of_types())}
        self.__entities = {e_type: {} for e_type in range(EntityType.num_of_types())}

    def add(self, entity):
        """
        Add entity to container (add only one entity without recursion)
        :param entity: entity to add
        :return: entity id in container
        """
        e_type = EntityType.from_instance(entity)
        if e_type is None:
            return None
        e_id = self.__cur_ids[e_type]
        self.__entities[e_type][e_id] = entity
        self.__cur_ids[e_type] += 1
        return e_id

    def get(self, e_type: int, e_id):
        """
        Get entity of type by id in container
        :param e_type: enum value type of entity
        :param e_id: entity id in container
        """
        if e_type in EntityType.get_types() and e_id in self.__entities[e_type].keys():
            return self.__entities[e_type][e_id]
        else:
            return None

    def add_quest(self, quest):
        """
        Recursively add quest to container and change ids
        :param quest: quest to add to container
        """
        quest.quest_id = self.add(quest)
        for file in quest.files:
            file.file_id = self.add(file)
        for question in BFS(quest.first_question):
            question.question_id = self.add(question)
            for file in question.files:
                file.file_id = self.add(file)
            for hint in question.hints:
                for hint_file in hint.files:
                    hint_file.file_id = self.add(hint_file)
                hint.hint_id = self.add(hint)
            for answer in question.answers:
                answer.answer_option_id = self.add(answer)
            for movement in question.movements:
                movement.movement_id = self.add(movement)
                movement.place.place_id = self.add(movement.place)

    def remove(self, e_type: int, e_id: int):
        """
        Remove entity of type by id in container
        :param e_type: enum value type of entity
        :param e_id: entity id in container
        """
        if e_id not in self.__entities[e_type].keys():
            return

        entity = self.__entities[e_type].pop(e_id)

        if hasattr(entity, 'files'):
            for file in entity.files:
                self.__entities[EntityType.FILE].pop(file.file_id)
        if e_type == EntityType.QUEST:
            for question in BFS(entity.first_question):
                self.remove(EntityType.QUESTION, question.question_id)
        elif e_type == EntityType.QUESTION:
            for hint in entity.hints:
                self.remove(EntityType.HINT, hint)
            for ans in entity.answers:
                self.remove(EntityType.ANSWER, ans)
            for move in entity.hints:
                self.remove(EntityType.MOVEMENT, move)
        elif e_type == EntityType.MOVEMENT:
            self.remove(EntityType.PLACE, entity.place)

        entity.remove_from_graph()

    def empty(self):
        """
        Check if there are no quests in container
        """
        return not self.__entities[EntityType.QUEST]
