from typing import Dict
from datetime import time

from copy import copy

from .db import get_quest, get_quest_tags, get_quest_rating, get_blocks, \
    check_uuid, add_media, set_quest, get_db, set_tags, set_rating, \
    set_block, add_hint, add_answer, add_place, set_blocks_link, set_answer_and_block_link

from uuid import uuid4


class Media:
    unic_id = 0

    class Type:
        IMAGE = 0,
        VIDEO = 1,
        AUDIO = 2

        @staticmethod
        def get_type_by_name(type: str) -> int:
            if type == "image":
                return Media.Type.IMAGE
            elif type == "video":
                return Media.Type.VIDEO
            elif type == "audio":
                return Media.Type.AUDIO
            else:
                return None
            
        @staticmethod
        def get_type_name(type: int) -> str:
            if type == Media.Type.IMAGE:
                return "image"
            elif type == Media.Type.VIDEO:
                return "video"
            elif type == Media.Type.AUDIO:
                return "audio"
            else:
                return None

    def __init__(self) -> None:
        self.id = copy(Media.unic_id)
        self.media_path = None
        self.media_type_id = None

        Media.unic_id += 1
        
    def convert_to_dict(self):
        return {"media_id": self.id,
                "media_path": self.media_path,
                "media_type_name": Media.Type.get_type_name(self.media_type_id)}
    
    def add_to_db(self, table_name: str, object_type: str, object_id: int) -> bool:
        return add_media(table_name, self.media_path, self.media_type_id, object_type, object_id)

    def update_from_dict(self, media_info: dict) -> int:
        try:
            for attr, value in media_info.items():
                if attr == "media_type_name":
                    self.media_type_id = Media.Type.get_type_by_name(value)
                else:
                    self.__setattr__(attr, value)

            if not self.media_type_id:
                return None
        except:
            return None
        
        return self.id
    
class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Block:
    class Type:
        START = 0
        OPEN = 1
        CHOICE = 2
        MOVEMENT = 3
        MESSAGE = 4
        END = 5

        @staticmethod
        def get_type_by_name(type_name: str) -> int:
            if type_name == "start_block":
                return Block.Type.START
            elif type_name == "open_question":
                return Block.Type.OPEN
            elif type_name == "choice_question":
                return Block.Type.CHOICE
            elif type_name == "movement":
                return Block.Type.MOVEMENT
            elif type_name == "message":
                return Block.Type.MESSAGE
            elif type_name == "end_block":
                return Block.Type.END
            else:
                return None
            
        @staticmethod
        def get_name_by_type(type: int) -> str:
            if type == Block.Type.START:
                return "start_block"
            elif type == Block.Type.OPEN:
                return "open_question"
            elif type == Block.Type.CHOICE:
                return "choice_question"
            elif type == Block.Type.MOVEMENT:
                return "movement"
            elif type == Block.Type.MESSAGE:
                return "message"
            elif type == Block.Type.END:
                return "end_block"
            else:
                return None
    
    unic_id = 0

    def __init__(self):
        self.db_id = None
        self.id = copy(Block.unic_id)
        self.position = Position(0., 0.)
        self.media_sources = {}
        self.text = ""
        self.next_block_id = None
        self.block_type_id = None

        Block.unic_id += 1

    def update_from_dict(self, block_info: dict) -> int:
        try:
            for attr, value in block_info.items():
                if attr == "pos_x":
                    self.position.x = block_info["pos_x"]
                elif attr == "pos_y":
                    self.position.y = block_info["pos_y"]
                elif attr == "block_type_name":
                    self.block_type_id = Information.Type.get_type_by_name(value)
                else:
                    self.__setattr__(attr, value)

            if not self.block_type_id:
                return None
        except:
            return None
        
        return self.id
    
    def add_media(self, media: Media):
        self.media_sources[media.id] = media

    def get_media_by_id(self, media_id: int) -> Media:
        return self.media_sources[media_id]
    
    def remove_media(self, media_id: int) -> bool:
        try:
            del self.media_sources[media_id]
        except:
            return False
        
        return True
    
    def convert_to_dict(self) -> dict:
        return {
            "block_id": self.id,
            "block_text": self.text,
            "block_type_name": Block.Type.get_name_by_type(self.block_type_id),
            "pos_x": self.position.x,
            "pos_y": self.position.y,
            "media_sources": [media.convert_to_dict() for media in self.media_sources],
            "next_block_id": self.next_block_id
        }
    
    def save_to_db(self, quest_id: int):
        set_block(self, quest_id)

        for media in self.media_sources.values():
            media.add_to_db("block_media", "block", self.db_id)

    def save_links_in_db(self, blocks: dict):
        if self.next_block_id != None:
            set_blocks_link(self.db_id, blocks[self.next_block_id].db_id)

class Answer:
    unic_id = 0

    def __init__(self) -> None:
        self.id = copy(Answer.unic_id)
        self.db_id = None
        self.option_text = None
        self.points = None
        self.next_block_id = None

        Answer.unic_id += 1

    def update_from_dict(self, answer_info: dict) -> int:
        try:
            for attr, value in answer_info.items():
                self.__setattr__(attr, value)
        except:
            return None
        
        return self.id
    
    def convert_to_dict(self) -> dict:
        return {
            'answer_option_id': self.id,
            'text': self.option_text,
            'points': self.points,
            'next_block_id': self.next_block_id if self.next_block_id is not None else None
        }
    
    def add_to_db(self, block_id: int):
        self.db_id = add_answer(self.option_text, self.points, block_id)

    def save_links_in_db(self, blocks: dict):
        if self.next_block_id != None:
            set_answer_and_block_link(self.db_id, blocks[self.next_block_id].db_id)

class Hint:
    unic_id = 0

    def __init__(self) -> None:
        self.db_id = None
        self.id = copy(Hint.unic_id)
        self.media_sources = {}
        self.text = ""
        self.fine = 0

        Hint.unic_id += 1

    def convert_to_dict(self):
        return {"hint_id": self.id,
                "hint_text": self.text,
                "fine": self.fine,
                "media_sources": [media.convert_to_dict() for media in self.media_sources.values()]}
    
    def add_media(self, media: Media) -> None:
        self.media_sources[media.id] = media

    def update_from_dict(self, hint_info: dict) -> int:
        try:
            for attr, value in hint_info.items():
                self.__setattr__(attr, value)
        except:
            return None
        
        return self.id
    
    def get_media_by_id(self, media_id):
        return self.media_sources[media_id]
    
    def remove_media(self, media_id: int) -> bool:
        try:
            del self.media_sources[media_id]
        except:
            return False
        
        return True
    
    def add_to_db(self, block_id: int):
        self.db_id = add_hint(self.text, self.fine, block_id)

        for media in self.media_sources.values():
            media.add_to_db("hint_media", "hint", self.db_id)

class Place:
    unic_id = 0

    def __init__(self) -> None:
        self.id = copy(Place.unic_id)
        self.latitude = None
        self.longitude = None
        self.radius = None
        self.time_open = None
        self.time_close = None

        Place.unic_id += 1

    def update_from_dict(self, place_info: dict) -> int:
        try:
            for attr, value in place_info.items():
                self.__setattr__(attr, value)
        except:
            return None
        
        return self.id
    
    def convert_to_dict(self) -> dict:
        return {
            'place_id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius': self.radius,
            'time_open': self.time_open, 
            'time_close': self.time_close
        }
    
    def add_to_db(self, block_id: int):
        add_place(self.latitude, self.longitude, self.radius, self.time_open, self.time_close, block_id)

class Information(Block):
    def __init__(self):
        super().__init__()

class BlockWithHint(Block):
    def __init__(self):
        super().__init__()
        self.hints = {}

    def add_hint(self, hint: Hint):
        self.hints[hint.id] = hint

    def remove_hint(self, hint_id: int) -> bool:
        try:
            del self.hints[hint_id]
        except:
            return False
        
        return True

    def get_hint_by_id(self, hint_id):
        return self.hints[hint_id]
    
    def convert_to_dict(self) -> dict:
        block_dict = super().convert_to_dict()

        block_dict["hints"] = [hint.convert_to_dict() for hint in self.hints.values()]

        return block_dict
    
    def save_to_db(self, quest_id: int):
        super().save_to_db(quest_id)
        for hint in self.hints.values():
            hint.add_to_db(self.db_id)
        
class Question(BlockWithHint):
    def __init__(self):
        super().__init__()
        self.answers = {}
    
    def get_answer_by_id(self, answer_id):
        return self.answers[answer_id]
    
    def add_answer(self, answer: Answer) -> None:
        self.answers[answer.id] = answer

    def remove_answer(self, answer_id: int) -> bool:
        try:
            del self.answers[answer_id]
        except:
            return False
        
        return True
    
    def convert_to_dict(self) -> dict:
        block_dict = super().convert_to_dict()

        block_dict["answers"] = [answer.convert_to_dict() for answer in self.answers.values()]

        return block_dict
    
    def save_to_db(self, quest_id: int):
        super().save_to_db(quest_id)
        for answer in self.answers.items():
            answer.add_to_db(self.db_id)

    def save_links_in_db(self, blocks: dict):
        for answer in self.answers.items():
            answer.save_links_in_db(blocks)

class Movement(BlockWithHint):
    def __init__(self):
        super().__init__()
        self.place = None
        self.block_type_id = Block.Type.MOVEMENT

    def add_place(self, place: Place):
        self.place = place

    def convert_to_dict(self) -> dict:
        block_dict = super().convert_to_dict()

        block_dict["place"] = self.place.convert_to_dict() if self.place != None else None

        return block_dict
    
    def save_to_db(self, quest_id: int):
        super().save_to_db(quest_id)
        self.place.add_to_db(self.db_id)

class Quest:
    def __init__(self) -> None:
        self.blocks = {}
        self.id = None
        self.title = None
        self.author_id = None
        self.description = None
        self.keyword = str(uuid4())[:8]
        while not check_uuid(self.keyword):
            self.keyword = str(uuid4())[:8]
        self.password = None
        self.cover_path = None
        self.hidden = False
        self.published = False
        self.tags = []
        self.rating = {'one': 0, 'two': 0, 'three': 0, 'four': 0, 'five': 0}

    def init_from_db(self, id: int):
        quest_info = get_quest(quest_id=id)
        if not quest_info:
            return False
        
        self.id = id
        self.title = quest_info['title']
        self.author_id = quest_info['author_id']
        self.description = quest_info['description']
        self.keyword = quest_info['keyword']
        self.password = quest_info['password']
        self.cover_path = quest_info['cover_path']
        self.hidden = quest_info['hidden']
        self.published = quest_info['published']
        self.tags = [tag['tag_name'] for tag in get_quest_tags(id)]
        self.rating = get_quest_rating(id)

        blocks_info = get_blocks(id)
        for block_info in blocks_info:
            block = self.__create_block__(block_info)
            self.blocks.update({block_info["block_id"]: block})

        return True

    @staticmethod
    def __create_block__(block_info: dict):
        block = None
        block_type = block_info["block_type_name"]

        if block_type == "start_block":
            block = Information(block_info["block_id"], )

        return block

    def add_block(self, block: Block) -> None:
        self.blocks[block.id] = block

    def remove_block_by_id(self, block_id: int) -> bool:
        try:
            del self.blocks[block_id]
        except:
            return False
        
        return True

    def get_block_by_id(self, block_id: int) -> Block:
        try:
            block = self.blocks[block_id]
        except:
            return None
        
        return block

    def convert_to_dict(self):
        quest_dict = {}

        quest_dict['quest_id'] = self.id
        quest_dict['title'] = self.title
        quest_dict['tags'] = self.tags
        quest_dict['hidden'] = self.hidden
        quest_dict['description'] = self.description
        quest_dict['password'] = self.password
        quest_dict['blocks'] = []
        for block in self.blocks.values():
            quest_dict['blocks'].append(block.convert_to_dict())

        return quest_dict

    def init_from_dict(self, quest_info: dict) -> bool:
        if 'title' not in quest_info.keys():
            return False
        rc = self.update_from_dict(quest_info)
        if not rc:
            return False
        start = Information()
        start.update_from_dict({
            "pos_x": 500,
            "pos_y": 320,
            "block_type_name": "start_block"
        })
        end = Information()
        end.update_from_dict({
            "pos_x": 800,
            "pos_y": 320,
            "block_type_name": "end_block"
        })
        start.next_block_id = end.id

        self.blocks[start.id] = start
        self.blocks[end.id] = end

        return True

    def update_from_dict(self, quest_info: dict) -> bool:
        try:
            for attr, value in quest_info.items():
                self.__setattr__(attr, value)
        except:
            return False
        
        return True

    def save_to_db(self) -> bool:
        try:
            set_quest(self) 

            if self.id is None:
                return False
            
            set_tags(self.tags, self.id)
            set_rating(self.id, self.rating)
            for block in self.blocks.values():
                block.save_to_db(self.id)
            for block in self.blocks.values():
                block.save_links_in_db(self.blocks)

        except Exception as err:
            print(err)
            return False
        else:
            get_db().commit()
        
        return True

    def __del__(self):
        Media.unic_id = 0
        Block.unic_id = 0
        Answer.unic_id = 0
        Hint.unic_id = 0
        Place.unic_id = 0