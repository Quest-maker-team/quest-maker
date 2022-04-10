from .quest import Quest, Question, Place, Hint, Answer, Movement, File, update_from_dict
from .entities_container import EntityType, EntitiesContainer
from flask_login import current_user, login_required

from flask import Blueprint, jsonify, request, g

import pickle
import os

api = Blueprint('api', __name__)


@api.before_request
@login_required
def before_request():
    """
    Check auth and load user's container with draft quests
    """
    author_id = current_user.author['author_id']
    path = f'quest_containers/{author_id}'
    if os.path.exists(path):
        with open(path, 'rb') as file:
            g.container = pickle.load(file)
    else:
        g.container = EntitiesContainer()


@api.after_request
@login_required
def after_request(response):
    """
    Serialize container with draft quests
    """
    author_id = current_user.author['author_id']
    path = f'quest_containers/{author_id}'
    if 'container' in g:
        if g.container.empty():
            if os.path.exists(path):
                os.remove(path)
        else:
            with open(path, 'wb') as file:
                pickle.dump(g.container, file)
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
    g.container.add_quest(quest)
    return jsonify(quest.to_dict())


@api.route('/draft/quest/<int:quest_id>', methods=['GET'])
def get_quest_from_draft(quest_id):
    """
    Get draft quest
    :param quest_id: quest id in container
    :return: json with quest or error message
    """
    quest = g.container.get(EntityType.QUEST, quest_id)
    return jsonify(quest.to_dict()) if quest else ('Wrong quest id', 400)


@api.route('/quest', methods=['POST'])
def create_quest():
    """
    Create new draft quest and add to container
    :return: json or error message
    """
    quest_dict = request.get_json(force=True)
    quest = Quest()
    rc = quest.create_from_dict(quest_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    g.container.add_quest(quest)
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
    question = Question()
    rc = update_from_dict(question, question_dict)
    if not rc:
        return 'Wrong JSON attributes', 400

    question.question_id = g.container.add(question)
    return jsonify({'question_id': question.question_id})


@api.route('/answer_option/<int:answer_id>/question/<int:question_id>', methods=['PUT'])
def add_question_to_answer(answer_id, question_id):
    """
    Link answer and next question that was created before
    :param answer_id: answer id in container
    :param question_id: question id in container
    :return: status code
    """
    answer = g.container.get(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong answer id', 400
    question = g.container.get(EntityType.QUESTION, question_id)
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
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    question = g.container.get(EntityType.QUESTION, question_id)
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
    file = File()
    rc = update_from_dict(file, file_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    file.file_id = g.container.add(file)
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
    file = g.container.get(EntityType.FILE, file_id)
    if not file:
        return 'Wrong file id', 400

    e_type = EntityType.from_str(e_type_str)
    if e_type not in (EntityType.QUEST, EntityType.QUESTION, EntityType.HINT):
        return 'Bad Request', 400

    entity = g.container.get(e_type, e_id)
    if not entity:
        return f'Wrong {e_type_str} id', 400
    entity.files.append(file)
    file.parent = g.container.get(e_type, e_id)
    return '', 200


@api.route('/answer_option', methods=['POST'])
def create_answer():
    """
    Create new answer and add to container
    :return: json with answer id or error message
    """
    ans_dict = request.get_json(force=True)
    ans = Answer()
    rc = update_from_dict(ans, ans_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    ans.answer_option_id = g.container.add(ans)
    return jsonify({'answer_option_id': ans.answer_option_id})


@api.route('/question/<int:question_id>/answer_option/<int:answer_id>', methods=['PUT'])
def add_answer(question_id, answer_id):
    """
    Link question and answer that was created before
    :param question_id: question id in container
    :param answer_id: answer id in container
    :return: status code
    """
    answer = g.container.get(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong answer id', 400
    question = g.container.get(EntityType.QUESTION, question_id)
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
    move = Movement()
    rc = update_from_dict(move, move_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    move.movement_id = g.container.add(move)
    return jsonify({'movement_id': move.movement_id})


@api.route('/question/<int:question_id>/movement/<int:movement_id>', methods=['PUT'])
def add_movement(question_id, movement_id):
    """
    Link question and movement that was created before
    :param movement_id: movement id in container
    :param question_id: place id in container
    :return: status code
    """
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    question = g.container.get(EntityType.QUESTION, question_id)
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
    hint = Hint()
    rc = update_from_dict(hint, hint_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    hint.hint_id = g.container.add(hint)
    return jsonify({'hint_id': hint.hint_id})


@api.route('/question/<int:question_id>/hint/<int:hint_id>', methods=['PUT'])
def add_hint(question_id, hint_id):
    """
    Link question and hint that was created before
    :param question_id: question id in container
    :param hint_id: hint id in container
    :return: status code
    """
    hint = g.container.get(EntityType.HINT, hint_id)
    if not hint:
        return 'Wrong hint id', 400
    question = g.container.get(EntityType.QUESTION, question_id)
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
    place = Place()
    rc = update_from_dict(place, place_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    place.place_id = g.container.add(EntityType.PLACE, place)
    return jsonify({'place_id': place.place_id})


@api.route('/movement/<int:movement_id>/place/<int:place_id>', methods=['PUT'])
def add_place(movement_id, place_id):
    """
    Link movement and place that was created before
    :param movement_id: movement id in container
    :param place_id: place id in container
    :return: status code
    """
    place = g.container.get(EntityType.PLACE, place_id)
    if not place:
        return 'Wrong place id', 400
    movement = g.contaienr.get(EntityType.MOVEMENT, movement_id)
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
    rc = update_from_dict(g.container.get(e_type, e_id), e_dict)
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
    g.container.remove(e_type, e_id)
    return '', 200


@api.route('/answer_option/<int:answer_id>/question', methods=['DELETE'])
def remove_answer_question_link(answer_id):
    """
    Disconnect answer and next question
    :param answer_id: answer id in container
    :return: status code
    """
    answer = g.container.get(EntityType.ANSWER, answer_id)
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
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
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
    question = g.container.get(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
    if not movement:
        return 'Wrong movement id', 400
    if movement in question.movements:
        question.movements.remove(movement)
        movement.parent = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/question/<int:question_id>/answer/<int:answer_id>', methods=['DELETE'])
def remove_question_answer_link(question_id, answer_id):
    """
    Disconnect question and answer to this question
    :param question_id: question id in container
    :param answer_id: answer id in container
    :return: status code
    """
    question = g.container.get(EntityType.QUESTION, question_id)
    if not question:
        return 'Wrong question id', 400
    answer = g.container.get(EntityType.ANSWER, answer_id)
    if not answer:
        return 'Wrong movement id', 400
    if answer in question.answers:
        question.answers.remove(answer)
        answer.parent = None
        return '', 200
    else:
        return 'No link', 400


@api.route('/save/<int:quest_id>', methods=['POST'])
def save_quest(quest_id):
    """
    Save quest in database and remove from draft
    :param quest_id: quest_id in container
    :return: status code
    """
    author_id = current_user.author['author_id']
    quest = g.container.get(EntityType.QUEST, quest_id)
    if not quest:
        return 'Wrong quest id', 400
    quest.to_db(author_id)
    g.container.remove(EntityType.QUEST, quest_id)
    return '', 200
