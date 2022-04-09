from flask import Blueprint, jsonify, request, g
from .quest import Quest, Question, Place, Hint, Answer, Movement, File, update_from_dict
from .entities_container import EntityType, EntitiesContainer

import pickle
import os

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    author_id = 1
    path = f'quest_containers/{author_id}'
    if os.path.exists(path):
        with open(path, 'rb') as file:
            g.container = pickle.load(file)
    else:
        g.container = EntitiesContainer()


@api.after_request
def after_request(response):
    author_id = 1
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
    quest = Quest().from_db(quest_id)
    g.container.add_quest(quest)
    return jsonify(quest.to_dict())


@api.route('/draft/quest/<int:quest_id>', methods=['GET'])
def get_quest_from_draft(quest_id):
    return jsonify(g.container.get(EntityType.QUEST, quest_id).to_dict())


@api.route('/quest', methods=['POST'])
def create_quest():
    quest_dict = request.get_json(force=True)
    quest = Quest()
    rc = quest.create_from_dict(quest_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    g.container.add_quest(quest)
    return jsonify({'quest_id': quest.quest_id,
                    'start_question_id': quest.first_question.question_id,
                    'end_question_id': quest.first_question.answers[0].next_question.question_id})


@api.route('/question', methods=['POST'])
def create_question():
    question_dict = request.get_json(force=True)
    question = Question()
    rc = update_from_dict(question, question_dict)
    if not rc:
        return 'Wrong JSON attributes', 400

    question.question_id = g.container.add(question)
    return jsonify({'question_id': question.question_id})


@api.route('/answer_option/<int:answer_id>/question/<int:question_id>', methods=['PUT'])
def add_question_to_answer(answer_id, question_id):
    answer = g.container.get(EntityType.ANSWER, answer_id)
    question = g.container.get(EntityType.QUESTION, question_id)
    answer.next_question = question
    question.parents.append(answer)


@api.route('/movement/<int:movement_id>/question/<int:question_id>', methods=['PUT'])
def add_question_to_movement(movement_id, question_id):
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
    question = g.container.get(EntityType.QUESTION, question_id)
    movement.next_question = question
    question.parents.append(movement)


@api.route('/file', methods=['POST'])
def create_file():
    file_dict = request.get_json(force=True)
    file = File()
    rc = update_from_dict(file, file_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    file.file_id = g.container.add(file)
    return jsonify({'file_id': file.file_id})


@api.route('/<entity>/<int:e_id>/file/<int:file_id>', methods=['PUT'])
def add_file(entity, e_id, file_id):
    file = g.container.get(EntityType.FILE, file_id)

    e_type = EntityType.from_str(entity)
    if e_type not in (EntityType.QUEST, EntityType.QUESTION, EntityType.ANSWER, EntityType.HINT):
        return 'Bad Request', 400

    g.container.get(e_type, e_id).files.append(file)
    file.parent = g.container.get(e_type, e_id)


@api.route('/answer_option', methods=['POST'])
def create_answer():
    ans_dict = request.get_json(force=True)
    ans = Answer()
    rc = update_from_dict(ans, ans_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    ans.answer_option_id = g.container.add(ans)
    return jsonify({'answer_option_id': ans.answer_option_id})


@api.route('/question/<int:question_id>/answer_option/<int:answer_id>', methods=['PUT'])
def add_answer(question_id, answer_id):
    answer = g.container.get(EntityType.ANSWER, answer_id)
    question = g.container.get(EntityType.QUESTION, question_id)
    question.answers.append(answer)
    answer.parent = question


@api.route('/movement', methods=['POST'])
def create_movement():
    move_dict = request.get_json(force=True)
    move = Movement()
    rc = update_from_dict(move, move_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    move.movement_id = g.container.add(move)
    return jsonify({'movement_id': move.movement_id})


@api.route('/question/<int:question_id>/movement/<int:movement_id>', methods=['PUT'])
def add_movement(question_id, movement_id):
    movement = g.container.get(EntityType.MOVEMENT, movement_id)
    question = g.container.get(EntityType.QUESTION, question_id)
    question.movements.append(movement)
    movement.parent = question


@api.route('/hint', methods=['POST'])
def create_hint():
    hint_dict = request.get_json(force=True)
    hint = Hint()
    rc = update_from_dict(hint, hint_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    hint.hint_id = g.container.add(hint)
    return jsonify({'hint_id': hint.hint_id})


@api.route('/question/<int:question_id>/hint/<int:hint_id>', methods=['PUT'])
def add_hint(question_id, hint_id):
    hint = g.container.get(EntityType.HINT, hint_id)
    question = g.container.get(EntityType.QUESTION, question_id)
    question.hints.append(hint)
    hint.parent = question


@api.route('/place', methods=['POST'])
def create_place():
    place_dict = request.get_json(force=True)
    place = Place()
    rc = update_from_dict(place, place_dict)
    if not rc:
        return 'Wrong JSON attributes', 400
    place.place_id = g.container.add(EntityType.PLACE, place)
    return jsonify({'place_id': place.place_id})


@api.route('/movement/<int:movement_id>/place/<int:place_id>', methods=['PUT'])
def add_place(movement_id, place_id):
    place = g.container.get(EntityType.PLACE, place_id)
    movement = g.contaienr.get(EntityType.MOVEMENT, movement_id)
    movement.place = place
    place.parent = movement


@api.route('/<e_type_str>/<int:e_id>', methods=['PUT'])
def update_entity(e_type_str, e_id):
    e_dict = request.get_json(force=True)
    e_type = EntityType.from_str(e_type_str)
    if e_type is None:
        return 'Bad Request', 400
    rc = update_from_dict(g.container.get(e_type, e_id), e_dict)
    return ('', 200) if rc else ('Wrong JSON attributes', 400)


@api.route('/<e_type_str>/<int:e_id>', methods=['DELETE'])
def remove_entity(e_type_str, e_id):
    e_type = EntityType.from_str(e_type_str)
    if e_type is None:
        return 'Bad Request', 400
    g.container.remove(e_type, e_id)


@api.route('/save/<int:quest_id>', methods=['POST'])
def save_quest(quest_id):
    author_id = 1
    g.container.get(EntityType.QUEST, quest_id).to_db(author_id)
    g.container.remove(EntityType.QUEST, quest_id)
    return '', 200


@api.route('/check/<int:q_id>', methods=['GET'])
def check(q_id):
    return jsonify(g.container.get(EntityType.QUEST, q_id).to_dict())
