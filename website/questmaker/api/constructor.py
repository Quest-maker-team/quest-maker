from website.questmaker.db import get_draft, update_draft, write_draft, remove_draft, get_draft_for_update
from website.questmaker.quest import Quest, Information, Question, Movement, Block, Answer, Media, Hint, Place

from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request, g, session

import pickle


constructor_api = Blueprint('constructor_api', __name__)


@constructor_api.before_request
@login_required
def before_request():
    """
    Check auth and load user's container with draft quest
    """
    author_id = current_user.id
    if request.method == 'GET' or \
            (request.method == 'POST' and request.endpoint in ['constructor_api.create_quest',
                                                               'constructor_api.save_quest']):
        return
    if 'draft_id' in session:
        draft = get_draft_for_update(session['draft_id'])
        if not draft:
            return 'No draft with this id', 400
        if draft['author_id'] != author_id:
            return 'This is not your quest', 403
        g.container = pickle.loads(bytes(draft['container']))
    else:
        return 'You don\'t have loaded draft', 400


@constructor_api.after_request
@login_required
def after_request(response):
    """
    Serialize container with draft quests and write to db
    """
    if request.method == 'GET' or \
            (request.method == 'POST' and request.endpoint in ['constructor_api.create_quest',
                                                               'constructor_api.save_quest']):
        return response
    if 'container' in g and 'draft_id' in session:
        update_draft(session['draft_id'], pickle.dumps(g.container))
    elif 'container' in g and 'draft_id' not in session:
        return 'Could not save changes. Perhaps cookies are disabled.', 400

    return response


@constructor_api.route('/quest/<int:quest_id>', methods=['GET'])
def get_quest(quest_id):
    """
    Get quest for edit from drafts if draft exists or create new draft
    """
    draft = get_draft(quest_id)
    if draft:
        if draft['author_id'] != current_user.id:
            return 'This is not your quest', 403
        quest = pickle.loads(bytes(draft['container']))
        session['draft_id'] = draft['draft_id']
        return jsonify(quest.convert_to_dict()) if type(quest).__name__ == Quest.__name__ else ('Wrong quest id', 400)
    else:
        return get_quest_from_db(quest_id)
    
def get_quest_from_db(quest_id):
    """
    Load quest from database to constructor
    :param quest_id: quest id in database
    :return: json with quest or error message
    """
    quest = Quest()
    
    if not quest.init_from_db(quest_id):
        return 'Wrong quest id', 400
    if quest.author_id != current_user.id:
        return 'This is not your quest', 403

    draft_id = write_draft(current_user.id, pickle.dumps(quest), quest_id)
    session['draft_id'] = draft_id
    return jsonify(quest.convert_to_dict())


@constructor_api.route('/quest', methods=['POST'])
def create_quest():
    """
    Create new draft quest and add to container
    :return: json or error message
    """
    quest_dict = request.get_json(force=True)
    quest = Quest()
    if not quest.init_from_dict(quest_dict):
        return 'Wrong JSON attributes', 400
    quest.author_id = current_user.id

    if not quest.save_to_db():
        return 'Internal Server Error', 500

    draft_id = write_draft(current_user.id, pickle.dumps(quest), quest.quest_id)
    session['draft_id'] = draft_id
    return jsonify(quest.convert_to_dict())

def init_block(request, block: Block):
    block_dict = request.get_json(force=True)

    block_id = block.update_from_dict(block_dict)
    if block_id is None:
        return 'Wrong JSON attributes', 400

    g.container.add_block(block)
    return jsonify({'question_id': block_id})

@constructor_api.route('/question_block', methods=['POST'])
def create_question_block():
    """
    Create new question block and add to quest
    :return: json with block id or error message
    """
    block = Question()
    return init_block(request, block)

@constructor_api.route('/movement_block', methods=['POST'])
def create_movement_block():
    """
    Create new movement block and add to quest
    :return: json with block id or error message
    """
    block = Movement()
    return init_block(request, block)

@constructor_api.route('/information_block', methods=['POST'])
def create_information_block():
    """
    Create new information block and add to quest
    :return: json with block id or error message
    """
    block = Information()
    return init_block(request, block)
    
@constructor_api.route('/answer_host/<int:host_id>/answer_id/<int:answer_id>/block/<int:block_id>', methods=['PUT'])
def connect_answer_and_block(host_id, answer_id, block_id):
    """
    Link answer and next question that was created before
    :param answer_id: answer id in container
    :param question_id: question id in container
    :return: status code
    """
    host_block = g.container.get_block_by_id(host_id)
    if not host_block or type(host_block) != Question:
        return 'Wrong host_block id', 400
    
    answer = host_block.get_answer_by_id(answer_id)
    if not answer:
        return 'Wrong answer id', 400

    block = g.container.get_block_by_id(block_id)
    if not block:
        return 'Wrong block id', 400
    
    answer.next_block_id = block_id
    return '', 200
    
@constructor_api.route('/source_block/<int:source_id>/target_block/<int:target_id>', methods=['PUT'])
def connect_blocks(source_id, target_id):
    """
    Link two blocks that was created before
    :param source_id: block id in quest
    :param question_id: block id in quest
    :return: status code
    """
    source_block = g.container.get_block_by_id(source_id)
    if not source_block:
        return 'Wrong source id', 400
    
    target_block = g.container.get_block_by_id(target_id)
    if not target_block:
        return 'Wrong target id', 400
    
    source_block.next_block_id = target_id
    return '', 200

@constructor_api.route('/media/block/<int:block_id>', methods=['POST'])
def create_block_media(block_id):
    """
    Create new media and add to block
    :return: json with media id or error message
    """
    media_dict = request.get_json(force=True)

    media = Media()
    media_id = media.update_from_dict(media_dict)
    if not media_id:
        return 'Wrong JSON attributes', 400
    
    block = g.container.get_block_by_id(block_id)
    if not block:
        return 'Wrong block id', 400
    
    block.add_media(media)

    return jsonify({'media_id': media.id})

@constructor_api.route('/media/block/<int:block_id>/hint/<int:hint_id>', methods=['POST'])
def create_hint_media(block_id, hint_id):
    """
    Create new media and add to block's hint
    :return: json with media id or error message
    """
    media_dict = request.get_json(force=True)

    media = Media()
    media_id = media.update_from_dict(media_dict)
    if not media_id:
        return 'Wrong JSON attributes', 400
    
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    hint = block.get_hint_by_id(hint_id)
    if not hint:
        return 'Wrong hint id', 400
    
    hint.add_media(media)

    return jsonify({'media_id': media_id})

@constructor_api.route('/answer_option/question/<int:question_id>', methods=['POST'])
def create_question_answer(block_id):
    """
    Create new question answer and add to question
    :return: json with answer id or error message
    """
    ans_dict = request.get_json(force=True)
    answer = Answer()
    answer_id = answer.update_from_dict(ans_dict)
    if not answer_id:
        return 'Wrong JSON attributes', 400
    
    question = g.container.get_block_by_id(block_id)
    if not question or type(question) != Question:
        return 'Wrong block id', 400

    question.add_answer(answer)

    return jsonify({'answer_option_id': answer_id})

@constructor_api.route('/hint/block/<int:block_id>', methods=['POST'])
def create_hint(block_id):
    """
    Create new hint and add to block
    :return: json with hint id or error message
    """
    hint_dict = request.get_json(force=True)

    hint = Hint()

    hint_id = hint.update_from_dict(hint_dict)
    if not hint_id:
        return 'Wrong JSON attributes', 400
    
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    block.add_hint(hint)

    return jsonify({'hint_id': hint.id})

@constructor_api.route('/place/movement_block/<int:block_id>', methods=['POST'])
def create_place(block_id):
    """
    Create new place and add to movement_block
    :return: json with hint id or error message
    """
    place_dict = request.get_json(force=True)

    place = Place()

    place_id = place.update_from_dict(place_dict)
    if not place:
        return 'Wrong JSON attributes', 400
    
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Movement:
        return 'Wrong block id', 400
    
    block.add_place(place)

    return jsonify({'hint_id': place_id})

@constructor_api.route('/block/<int:block_id>', methods=['PUT'])
def update_block(block_id):
    """
    Set block attributes from JSON
    :param block_id: block id in quest
    :return: status code
    """
    block_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block:
        return 'Wrong block id', 400
    
    rc = block.update_from_dict(block_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>/media/<int:media_id>', methods=['PUT'])
def update_block_media(block_id, media_id):
    """
    Set block media attributes from JSON
    :param block_id: block id in quest
    :param media_id: media id in block
    :return: status code
    """
    media_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block:
        return 'Wrong block id', 400
    
    media = block.get_media_by_id(media_id)
    if not media:
        return 'Wrong media id', 400
    rc = media.update_from_dict(media_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>/hint/<int:hint_id>/media/<int:media_id>', methods=['PUT'])
def update_hint_media(block_id, hint_id, media_id):
    """
    Set block media attributes from JSON
    :param block_id: block id in quest
    :param hint_id: hint id in block
    :param media_id: media id in hint
    :return: status code
    """
    media_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    hint = block.get_hint_by_id(hint_id)
    if not hint:
        return 'Wrong media id', 400
    
    media = hint.get_media_by_id(media_id)
    if not media:
        return 'Wrong media id', 400
    
    rc = media.update_from_dict(media_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>/answer/<int:answer_id>', methods=['PUT'])
def update_block_answer(block_id, answer_id):
    """
    Set block answer attributes from JSON
    :param block_id: block id in quest
    :param answer_id: answer id in block
    :return: status code
    """
    answer_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question:
        return 'Wrong block id', 400
    
    answer = block.get_answer_by_id(answer_id)
    if not answer:
        return 'Wrong media id', 400
    rc = answer.update_from_dict(answer_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>/hint/<int:hint_id>', methods=['PUT'])
def update_block_hint(block_id, hint_id):
    """
    Set block media attributes from JSON
    :param block_id: block id in quest
    :param hint_id: hint id in block
    :return: status code
    """
    hint_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    hint = block.get_hint_by_id(hint_id)
    if not hint:
        return 'Wrong media id', 400
    rc = hint.update_from_dict(hint_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>/place/<int:place_id>', methods=['PUT'])
def update_block_place(block_id, place_id):
    """
    Set block media attributes from JSON
    :param block_id: block id in quest
    :param place_id: place id in block
    :return: status code
    """
    place_dict = request.get_json(force=True)
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Movement:
        return 'Wrong block id', 400
    
    place = block.get_hint_by_id(place_id)
    if not place:
        return 'Wrong media id', 400
    rc = place.update_from_dict(place_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/quest>', methods=['PUT'])
def update_quest():
    """
    Set quest attributes from JSON
    :return: status code
    """
    quest_dict = request.get_json(force=True)
    rc = g.container.update_from_dict(quest_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)

@constructor_api.route('/block/<int:block_id>', methods=['DELETE'])
def remove_block(block_id):
    """
    Remove block from quest graph
    :param block_id: block id in quest
    :return: status code
    """
    rc = g.container.remove_block_by_id(block_id)
    return ('', 200) if rc else ('Wrong block id', 400)

@constructor_api.route('/block/<int:block_id>/media/<int:media_id>', methods=['DELETE'])
def remove_block_media(block_id, media_id):
    """
    Remove media from block
    :param block_id: block id in quest
    :param media_id: media id in quest
    :return: status code
    """
    block = g.container.get_block_by_id(block_id)
    if not block:
        return 'Wrong block id', 400
    rc = block.remove_media(media_id)
    return ('', 200) if rc else ('Wrong media id', 400)

@constructor_api.route('/block/<int:block_id>/hint/<int:hint_id>/media/<int:media_id>', methods=['DELETE'])
def remove_hint_media(block_id, hint_id, media_id):
    """
    Remove media from block
    :param block_id: block id in quest
    :param hint_id: hint id in block
    :param media_id: media id in quest
    :return: status code
    """
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    hint = block.get_hint_by_id(hint_id)
    if not hint:
        return 'Wrong media id', 400
    
    rc = hint.remove_media(media_id)
    return ('', 200) if rc else ('Wrong media id', 400)

@constructor_api.route('/block/<int:block_id>/answer/<int:answer_id>', methods=['DELETE'])
def remove_block_answer(block_id, answer_id):
    """
    Remove answer from block
    :param block_id: block id in quest
    :param answer_id: answer id in quest
    :return: status code
    """
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question:
        return 'Wrong block id', 400
    rc = block.remove_answer(answer_id)
    return ('', 200) if rc else ('Wrong media id', 400)

@constructor_api.route('/block/<int:block_id>/hint/<int:hint_id>', methods=['DELETE'])
def remove_hint(block_id, hint_id):
    """
    Remove hint from block
    :param block_id: block id in quest
    :param hint_id: hint id in block
    :return: status code
    """
    block = g.container.get_block_by_id(block_id)
    if not block or type(block) != Question and type(block) != Movement:
        return 'Wrong block id', 400
    
    rc = block.remove_hint(hint_id)
    return ('', 200) if rc else ('Wrong media id', 400)

@constructor_api.route('/answer_host/<int:host_id>/answer_id/<int:answer_id>', methods=['PUT'])
def disconnect_answer_and_block(host_id, answer_id):
    """
    Unlink answer and next question that was created before
    :param host_id: host block id in container
    :param answer_id: answer id in container
    :return: status code
    """
    host_block = g.container.get_block_by_id(host_id)
    if not host_block or type(host_block) != Question:
        return 'Wrong host_block id', 400
    
    answer = host_block.get_answer_by_id(answer_id)
    if not answer:
        return 'Wrong answer id', 400
    
    answer.next_block_id = None
    return '', 200
    
@constructor_api.route('/source_block/<int:source_id>', methods=['PUT'])
def disconnect_blocks(source_id):
    """
    Unlink two blocks that was created before
    :param source_id: block id in quest
    :param question_id: block id in quest
    :return: status code
    """
    source_block = g.container.get_block_by_id(source_id)
    if not source_block:
        return 'Wrong source id', 400
    
    source_block.next_block_id = None
    return '', 200

@constructor_api.route('/save/<int:quest_id>', methods=['POST'])
def save_quest(quest_id):
    """
    Save quest in database and remove from drafts
    :param quest_id: quest id in quests and drafts
    :return: status code
    """
    author_id = current_user.id
    draft = get_draft(quest_id)
    if not draft:
        return 'No quest with this id', 400
    if draft['author_id'] != author_id:
        return 'This is not your quest', 403
    quest = pickle.loads(bytes(draft['container']))
    quest.published = True
    quest.save_to_db()
    remove_draft(quest_id)
    if 'draft_id' in session:
        session.pop('draft_id')
    return '', 200
