from .quest import Quest, Question, Place, Hint, Answer, Movement, File, update_from_dict
from .quest_container import EntityType, QuestContainer
from .db import get_draft, update_draft, write_draft, remove_draft, get_draft_for_update
from flask_login import current_user, login_required

from flask import Blueprint, jsonify, request, g, session

import pickle

api = Blueprint('api', __name__)


@api.before_request
@login_required
def before_request():
    """
    Check auth and load user's container with draft quest
    """
    author_id = current_user.author['author_id']
    if request.method == 'GET' or \
            (request.method == 'POST' and request.endpoint in ['api.create_quest', 'api.save_quest']):
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


@api.after_request
@login_required
def after_request(response):
    """
    Serialize container with draft quests and write to db
    """
    if request.method == 'GET' or \
            (request.method == 'POST' and request.endpoint in ['api.create_quest', 'api.save_quest']):
        return response
    if 'container' in g and 'draft_id' in session:
        update_draft(session['draft_id'], pickle.dumps(g.container))
    elif 'container' in g and 'draft_id' not in session:
        return 'Could not save changes. Perhaps cookies are disabled.', 400

    return response


@api.route('/db/quest/<int:quest_id>', methods=['GET'])
def get_quest_from_db(quest_id):
    """
    Load quest from database to constructor
    :param quest_id: quest id in database
    :return: json with quest or error message
    """
    quest = Quest().from_db(quest_id)
    if not quest:
        return 'Wrong quest id', 400
    if quest.author_id != current_user.author['author_id']:
        return 'This is not your quest', 403

    container = QuestContainer()
    container.add_quest(quest)
    quest.quest_id = write_draft(current_user.author['author_id'], pickle.dumps(container))
    session['draft_id'] = quest.quest_id
    return jsonify(quest.to_dict())


@api.route('/draft/quest/<int:draft_id>', methods=['GET'])
def get_quest_from_draft(draft_id):
    """
    Get draft quest
    :param draft_id: draft id in drafts table
    :return: json with quest or error message
    """
    draft = get_draft(draft_id)
    if not draft:
        return 'Draft does not exist', 400
    if draft['author_id'] != current_user.author['author_id']:
        return 'This is not your quest', 403
    quest = pickle.loads(bytes(draft['container'])).quest
    session['draft_id'] = draft_id
    return jsonify(quest.to_dict()) if quest else ('Wrong quest id', 400)


@api.route('/quest', methods=['POST'])
def create_quest():
    """
    Create new draft quest and add to container
    :return: json or error message
    """
    quest_dict = request.get_json(force=True)
    if not Quest.check_creation_attrs(quest_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    quest = Quest()
    rc = quest.create_from_dict(quest_dict)
    if not rc:
        return 'Wrong JSON attributes', 400

    container = QuestContainer()
    container.add_quest(quest)
    draft_id = write_draft(current_user.author['author_id'], pickle.dumps(container))
    quest.quest_id = draft_id
    session['draft_id'] = draft_id
    return jsonify({'quest_id': quest.quest_id,
                    'start_question_id': quest.first_question.question_id,
                    'first_answer_id': quest.first_question.answers[0].answer_option_id,
                    'end_question_id': quest.first_question.answers[0].next_question.question_id})


@api.route('/question', methods=['POST'])
def create_question():
    """
    Create new question and add to container
    :return: json with question id or error message
    """
    question_dict = request.get_json(force=True)
    if not Question.check_creation_attrs(question_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    question = Question()
    rc = update_from_dict(question, question_dict)
    if not rc:
        return 'Wrong JSON attributes', 400

    question.question_id = g.container.add_entity(question)
    return jsonify({'question_id': question.question_id})


@api.route('/answer_option/<int:answer_id>/question/<int:question_id>', methods=['PUT'])
def add_question_to_answer(answer_id, question_id):
    """
    Link answer and next question that was created before
    :param answer_id: answer id in container
    :param question_id: question id in container
    :return: status code
    """
    answer = g.container.get_entity(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong answer id', 400
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    answer.next_question = question
    question.parents.append(answer)
    return '', 200


@api.route('/movement/<int:movement_id>/question/<int:question_id>', methods=['PUT'])
def add_question_to_movement(movement_id, question_id):
    """
    Link movement and next question that was created before
    :param movement_id: movement id in container
    :param question_id: question id in container
    :return: status code
    """
    movement = g.container.get_entity(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    movement.next_question = question
    question.parents.append(movement)
    return '', 200


@api.route('/file', methods=['POST'])
def create_file():
    """
    Create new file and add to container
    :return: json with file id or error message
    """
    file_dict = request.get_json(force=True)
    if not File.check_creation_attrs(file_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    file = File()
    rc = update_from_dict(file, file_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    file.file_id = g.container.add_entity(file)
    return jsonify({'file_id': file.file_id})


@api.route('/<e_type_str>/<int:e_id>/file/<int:file_id>', methods=['PUT'])
def add_file(e_type_str, e_id, file_id):
    """
    Add file tp entity. File must be created before.
    :param e_type_str: string name of entity
    :param e_id: entity id in container
    :param file_id: file id in container
    :return: status code
    """
    file = g.container.get_entity(EntityType.FILE, file_id)
    if not file:
        return 'Wrong file id', 400

    e_type = EntityType.from_str(e_type_str)
    if e_type not in (EntityType.QUEST, EntityType.QUESTION, EntityType.HINT):
        return 'Bad Request', 400

    entity = g.container.get_entity(e_type, e_id)
    if not entity:
        return f'Wrong {e_type_str} id', 400
    entity.files.append(file)
    file.parent = g.container.get_entity(e_type, e_id)
    return '', 200


@api.route('/answer_option', methods=['POST'])
def create_answer():
    """
    Create new answer and add to container
    :return: json with answer id or error message
    """
    ans_dict = request.get_json(force=True)
    if not Answer.check_creation_attrs(ans_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    ans = Answer()
    rc = update_from_dict(ans, ans_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    ans.answer_option_id = g.container.add_entity(ans)
    return jsonify({'answer_option_id': ans.answer_option_id})


@api.route('/question/<int:question_id>/answer_option/<int:answer_id>', methods=['PUT'])
def add_answer(question_id, answer_id):
    """
    Link question and answer that was created before
    :param question_id: question id in container
    :param answer_id: answer id in container
    :return: status code
    """
    answer = g.container.get_entity(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong answer id', 400
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    question.answers.append(answer)
    answer.parent = question
    return '', 200


@api.route('/movement', methods=['POST'])
def create_movement():
    """
    Create new answer and add to container
    :return: json with answer id or error message
    """
    move_dict = request.get_json(force=True)
    if not Movement.check_creation_attrs(move_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    move = Movement()
    rc = update_from_dict(move, move_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    move.movement_id = g.container.add_entity(move)
    return jsonify({'movement_id': move.movement_id})


@api.route('/question/<int:question_id>/movement/<int:movement_id>', methods=['PUT'])
def add_movement(question_id, movement_id):
    """
    Link question and movement that was created before
    :param movement_id: movement id in container
    :param question_id: place id in container
    :return: status code
    """
    movement = g.container.get_entity(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    question.movements.append(movement)
    movement.parent = question
    return '', 200


@api.route('/hint', methods=['POST'])
def create_hint():
    """
    Create new hint and add to container
    :return: json with hint id or error message
    """
    hint_dict = request.get_json(force=True)
    if not Hint.check_creation_attrs(hint_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    hint = Hint()
    rc = update_from_dict(hint, hint_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    hint.hint_id = g.container.add_entity(hint)
    return jsonify({'hint_id': hint.hint_id})


@api.route('/question/<int:question_id>/hint/<int:hint_id>', methods=['PUT'])
def add_hint(question_id, hint_id):
    """
    Link question and hint that was created before
    :param question_id: question id in container
    :param hint_id: hint id in container
    :return: status code
    """
    hint = g.container.get_entity(EntityType.HINT, hint_id)
    if not hint:
        return 'Wrong hint id', 400
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    question.hints.append(hint)
    hint.parent = question
    return '', 200


@api.route('/place', methods=['POST'])
def create_place():
    """
    Create new place and add to container
    :return: json with place id or error message
    """
    place_dict = request.get_json(force=True)
    if not Place.check_creation_attrs(place_dict.keys()):
        return 'Not enough JSON attributes for creating', 400
    place = Place()
    rc = update_from_dict(place, place_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    place.place_id = g.container.add_entity(place)
    return jsonify({'place_id': place.place_id})


@api.route('/movement/<int:movement_id>/place/<int:place_id>', methods=['PUT'])
def add_place(movement_id, place_id):
    """
    Link movement and place that was created before
    :param movement_id: movement id in container
    :param place_id: place id in container
    :return: status code
    """
    place = g.container.get_entity(EntityType.PLACE, place_id)
    if not place:
        return 'Wrong place id', 400
    movement = g.container.get_entity(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    movement.place = place
    place.parent = movement
    return '', 200


@api.route('/<e_type_str>/<int:e_id>', methods=['PUT'])
def update_entity(e_type_str, e_id):
    """
    Set entity attributes from JSON
    :param e_type_str: string name of entity
    :param e_id: entity id in container
    :return: status code
    """
    e_dict = request.get_json(force=True)
    e_type = EntityType.from_str(e_type_str)
    if e_type is None:
        return 'Bad Request', 400
    rc = update_from_dict(g.container.get_entity(e_type, e_id), e_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)


@api.route('/<e_type_str>/<int:e_id>', methods=['DELETE'])
def remove_entity(e_type_str, e_id):
    """
    Remove entity from quest graph
    :param e_type_str: string name of entity
    :param e_id: entity id in container
    :return: status code
    """
    e_type = EntityType.from_str(e_type_str)
    if e_type is None:
        return 'Bad Request', 400
    g.container.remove_entity(e_type, e_id)
    return '', 200


@api.route('/answer_option/<int:answer_id>/question', methods=['DELETE'])
def remove_answer_question_link(answer_id):
    """
    Disconnect answer and next question
    :param answer_id: answer id in container
    :return: status code
    """
    answer = g.container.get_entity(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong answer id', 400
    if answer.next_question:
        answer.next_question.parents.remove(answer)
        answer.next_question = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/movement/<int:movement_id>/question', methods=['DELETE'])
def remove_movement_question_link(movement_id):
    """
    Disconnect movement and next question
    :param movement_id: movement id in container
    :return: status code
    """
    movement = g.container.get_entity(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    if movement.next_question:
        movement.next_question.parents.remove(movement)
        movement.next_question = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/question/<int:question_id>/movement/<int:movement_id>', methods=['DELETE'])
def remove_question_movement_link(question_id, movement_id):
    """
    Disconnect question and movement of this question
    :param question_id: question id in container
    :param movement_id: movement id in container
    :return: status code
    """
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    movement = g.container.get_entity(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    if movement in question.movements:
        question.movements.remove(movement)
        movement.parent = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/question/<int:question_id>/answer_option/<int:answer_id>', methods=['DELETE'])
def remove_question_answer_link(question_id, answer_id):
    """
    Disconnect question and answer to this question
    :param question_id: question id in container
    :param answer_id: answer id in container
    :return: status code
    """
    question = g.container.get_entity(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    answer = g.container.get_entity(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong movement id', 400
    if answer in question.answers:
        question.answers.remove(answer)
        answer.parent = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/save/<int:draft_id>', methods=['POST'])
def save_quest(draft_id):
    """
    Save quest in database and remove from drafts
    :param draft_id: draft_id in drafts
    :return: status code
    """
    author_id = current_user.author['author_id']
    draft = get_draft(draft_id)
    if not draft:
        return 'No draft with this id', 400
    if draft['author_id'] != author_id:
        return 'This is not your quest', 403
    container = pickle.loads(bytes(draft['container']))
    container.quest.to_db()
    remove_draft(draft_id)
    return '', 200
