from typing import Dict
from datetime import time

from .db import *

from uuid import uuid4

import weakref
from copy import copy, deepcopy
from collections import deque


class Media:
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
        self.id = None
        self.media_path = None
        self.media_type_id = None

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
    
    def update_from_db_by_block(self, media_id: int) -> None:
        _, self.media_path, self.media_type_id, _ = get_block_media(media_id)

    def update_from_db_by_hint(self, media_id: int) -> None:
        _, self.media_path, self.media_type_id, _ = get_hint_media(media_id)
    
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
    
    def __init__(self):
        self.db_id = None
        self.id = None
        self.position = Position(0., 0.)
        self.media_sources = {}
        self.block_text = ""
        self.next_block = None
        self.block_type_id = None

    def update_from_dict(self, block_info: dict) -> int:
        try:
            for attr, value in block_info.items():
                if attr == "pos_x":
                    self.position.x = block_info["pos_x"]
                elif attr == "block_id":
                    self.db_id = block_info["block_id"]
                elif attr == "pos_y":
                    self.position.y = block_info["pos_y"]
                elif attr == "block_type_name":
                    self.block_type_id = Block.Type.get_type_by_name(value)
                else:
                    self.__setattr__(attr, value)

            if self.block_type_id == None:
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
            "block_text": self.block_text,
            "block_type_name": Block.Type.get_name_by_type(self.block_type_id),
            "pos_x": self.position.x,
            "pos_y": self.position.y,
            "media_sources": [media.convert_to_dict() for media in self.media_sources],
            "next_block_id": self.next_block().id if self.next_block is not None and self.next_block() is not None else None
        }
    
    def save_to_db(self, quest_id: int):
        set_block(self, quest_id)

        for media in self.media_sources.values():
            media.add_to_db("block_media", "block", self.db_id)

    def save_links_in_db(self, blocks: dict):
        if self.next_block is not None and self.next_block() is not None:
            set_blocks_link(self.db_id, blocks[self.next_block().id].db_id)

    def update_link_from_db(self, blocks_db_id: dict):
        next_block_id = get_link(self.db_id)[0]
        if next_block_id is not None:
            self.next_block = weakref.ref(blocks_db_id[next_block_id])

    def __getstate__(self):
        d = copy(self.__dict__)
        if self.next_block is not None:
            d["next_block"] = self.next_block()
        return d
    
    def __setstate__(self, d):
        self.__dict__ = d
        if self.next_block is not None:
            self.next_block = weakref.ref(self.next_block)

class Answer:
    def __init__(self) -> None:
        self.id = None
        self.db_id = None
        self.text = None
        self.points = None
        self.next_block = None

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
            'text': self.text,
            'points': self.points,
            'next_block_id': self.next_block().id if self.next_block is not None and self.next_block() is not None else None
        }
    
    def add_to_db(self, block_id: int):
        self.db_id = add_answer(self.text, self.points, block_id)

    def save_links_in_db(self, blocks: dict):
        if self.next_block is not None and self.next_block() is not None:
            set_answer_and_block_link(self.db_id, blocks[self.next_block().id].db_id)

    def update_from_db(self, answer_id: int) -> None:
        self.db_id, _, self.text, self.points, _ = get_answer_option(answer_id)

    def update_link_from_db(self, blocks_db_id: dict):
        next_block_id = get_answer_link(self.db_id)[0]
        if next_block_id is not None:
            self.next_block = weakref.ref(blocks_db_id[next_block_id])

    def __getstate__(self):
        d = copy(self.__dict__)
        if self.next_block is not None:
            d["next_block"] = self.next_block()
        return d
    
    def __setstate__(self, d):
        self.__dict__ = d
        if self.next_block is not None:
            self.next_block = weakref.ref(self.next_block)

class Hint:
    def __init__(self) -> None:
        self.db_id = None
        self.id = None
        self.media_sources = {}
        self.hint_text = ""
        self.fine = 0

    def convert_to_dict(self):
        return {"hint_id": self.id,
                "hint_text": self.hint_text,
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
        self.db_id = add_hint(self.hint_text, self.fine, block_id)

        for media in self.media_sources.values():
            media.add_to_db("hint_media", "hint", self.db_id)

    def update_from_db(self, hint_id: int) -> None:
        _, _, self.hint_text, self.fine = get_block_hint(hint_id)

        medias_info = get_hint_media_id(hint_id)
        for media_id in medias_info:
            media = Media()
            media.id = self.entity_id[Media.__name__]
            self.entity_id[Media.__name__] += 1
            media.update_from_db_by_hint(media_id)
            self.add_media(media)


class Place:
    def __init__(self) -> None:
        self.id = None
        self.latitude = None
        self.longitude = None
        self.radius = None
        self.time_open = None
        self.time_close = None

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

    def update_from_db(self, place_id: int) -> None:
        _, _, self.latitude, self.longitude, self.radius, self.time_open, self.time_close = get_block_place(place_id)

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
        for answer in self.answers.values():
            answer.add_to_db(self.db_id)

    def save_links_in_db(self, blocks: dict):
        for answer in self.answers.values():
            answer.save_links_in_db(blocks)

    def update_link_from_db(self, blocks_db_id: dict):
        for answer in self.answers.values():
            answer.update_link_from_db(blocks_db_id)

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

        self.entity_id = {
                Media.__name__: 0,
                Block.__name__: 0,
                Answer.__name__: 0,
                Hint.__name__: 0,
                Place.__name__: 0
            }

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
        blocks_db_id = {}
        for block_info in blocks_info:
            block = self.__create_block__(block_info)
            self.blocks.update({block.id: block})
            blocks_db_id[block_info["block_id"]] = block

        for block in self.blocks.values():
            block.update_link_from_db(blocks_db_id)

        return True

    def __create_block__(self, block_info: dict) -> Block:
        block = None
        block_type = Block.Type.get_type_by_name(block_info["block_type_name"])

        if block_type in [Block.Type.START, Block.Type.END, Block.Type.MESSAGE]:
            block = Information()
        elif block_type in [Block.Type.CHOICE, Block.Type.OPEN]:
            block = Question()
            answers_info = get_block_answer_option_id(block_info["block_id"])
            for answer_id in answers_info:
                answer = Answer()
                answer.id = self.entity_id[Answer.__name__]
                self.entity_id[Answer.__name__] += 1
                answer.update_from_db(answer_id)
                block.add_answer(answer)

        elif block_type == Block.Type.MOVEMENT:
            block = Movement()
            place_id = get_block_place_id(block_info["block_id"])
            print(block_info["block_id"])
            place = Place()
            place.id = self.entity_id[Place.__name__]
            self.entity_id[Place.__name__] += 1
            place.update_from_db(place_id)
            block.add_place(place)

        medias_info = get_block_media_id(block_info["block_id"])
        for media_id in medias_info:
            media = Media()
            media.id = self.entity_id[Media.__name__]
            self.entity_id[Media.__name__] += 1
            media.update_from_db_by_block(media_id)
            block.add_media(media)

        hints_info = get_block_hint_id(block_info["block_id"])
        for hint_id in hints_info:
            hint = Hint()
            hint.id = self.entity_id[Hint.__name__]
            self.entity_id[Hint.__name__] += 1
            hint.update_from_db(hint_id)
            block.add_hint(hint)

        block.id = self.entity_id[Block.__name__]
        self.entity_id[Block.__name__] += 1
        block.update_from_dict(block_info)

        return block

    def update_entity_unic_id(self, entity_name: str) -> None:
        self.entity_id[entity_name] += 1

    def get_entity_unic_id(self, entity_name: str) -> int:
        return self.entity_id[entity_name]

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
            "block_type_name": "start_block",
            "block_text": "Начало квеста"
        })
        start.id = self.entity_id[Block.__name__]
        self.entity_id[Block.__name__] += 1
        end = Information()
        end.update_from_dict({
            "pos_x": 800,
            "pos_y": 320,
            "block_type_name": "end_block",
            "block_text": "Конец квеста"
        })
        end.id = self.entity_id[Block.__name__]
        self.entity_id[Block.__name__] += 1

        start.next_block = weakref.ref(end)

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
    
    def check_reachability_all_blocks(self):
        start_block = None

        for block in self.blocks.values():
            if block.block_type_id == Block.Type.START:
                start_block = block
                break

        visited = []
        q = deque([start_block.id])

        while len(q) != 0:
            cur_block_id = q.popleft()
            visited.append(cur_block_id)

            is_added = False
            if self.blocks[cur_block_id].block_type_id == Block.Type.OPEN or self.blocks[cur_block_id].block_type_id == Block.Type.CHOICE:
                
                for answer in self.blocks[cur_block_id].answers.values():
                    if answer.next_block is not None and answer.next_block() is not None:
                        is_added = True
                        if answer.next_block().id not in visited:
                            q.appendleft(answer.next_block().id)
            else:
                if self.blocks[cur_block_id].next_block is not None and self.blocks[cur_block_id].next_block() is not None:
                    is_added = True
                    if self.blocks[cur_block_id].next_block().id not in visited:
                        q.appendleft(self.blocks[cur_block_id].next_block().id)

            if not is_added and self.blocks[cur_block_id].block_type_id != Block.Type.END:
                return False
    
        for block_id in self.blocks.keys():
            if block_id not in visited:
                return False
            
        return True

    def end_reachability_check(self):
        for block in self.blocks.values():
            visited = []
            q = deque([block.id])

            while len(q) != 0:
                cur_block_id = q.popleft()
                visited.append(cur_block_id)

                is_added = False
                if self.blocks[cur_block_id].block_type_id == Block.Type.OPEN or self.blocks[cur_block_id].block_type_id == Block.Type.CHOICE:
                    
                    for answer in self.blocks[cur_block_id].answers.values():
                        if answer.next_block is not None and answer.next_block() is not None:
                            is_added = True
                            if answer.next_block().id not in visited:
                                q.appendleft(answer.next_block().id)
                else:
                    if self.blocks[cur_block_id].next_block is not None and self.blocks[cur_block_id].next_block() is not None:
                        is_added = True
                        if self.blocks[cur_block_id].next_block().id not in visited:
                            q.appendleft(self.blocks[cur_block_id].next_block().id)

                if not is_added or len(q) == 0:
                    if self.blocks[cur_block_id].block_type_id != Block.Type.END:
                        return False
                    else:
                        break

        return True
    