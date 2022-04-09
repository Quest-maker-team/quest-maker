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


@api.route('/quest/<quest_id>', methods=['GET'])
def get_quest(quest_id):
    quest = Quest().from_db(quest_id)
    g.container.add_quest(quest)
    return jsonify(quest.to_dict())


@api.route('/quest', methods=['POST'])
def create_quest():
    quest_dict = request.get_json(force=True)
    quest = Quest()
    quest.create_from_dict(quest_dict)
    g.container.add_quest(quest)
    return jsonify({'quest_id': quest.quest_id,
                    'first_answer_id': quest.first_question.answers[0].answer_option_id})


@api.route('/answer_option/<int:answer_id>/question', methods=['POST'])
def add_question_to_answer(answer_id):
    question_dict = request.get_json(force=True)
    question = Question()
    update_from_dict(question, question_dict)

    question_id = g.container.add(question)
    question.question_id = question_id
    g.container.get(EntityType.ANSWER, answer_id).next_question = question

    return jsonify({'question_id': question_id})


@api.route('/movement/<int:movement_id>/question', methods=['POST'])
def add_question_to_movement(movement_id):
    question_dict = request.get_json(force=True)
    question = Question()
    update_from_dict(question, question_dict)

    question_id = g.container.add(question)
    question.question_id = question_id
    g.container.get(EntityType.MOVEMENT, movement_id).next_question = question

    return jsonify({'question_id': question_id})


@api.route('/<entity>/<int:e_id>/file', methods=['POST'])
def add_file(entity, e_id):
    file_dict = request.get_json(force=True)
    file = File()
    update_from_dict(file, file_dict)
    file_id = g.container.add(EntityType.FILE, file)

    e_type = EntityType.from_str(entity)
    if e_type not in (EntityType.QUEST, EntityType.QUESTION, EntityType.ANSWER, EntityType.HINT):
        return 'Bad Request', 400

    g.container.get(e_type, e_id).files.append(file)

    return jsonify({'file_id': file_id})


@api.route('/question/<int:question_id>/<e_type_str>', methods=['POST'])
def add_entity_to_question(question_id, e_type_str):
    if e_type_str == 'file':
        return add_file('question', question_id)
    e_dict = request.get_json(force=True)
    e_type = EntityType.from_str(e_type_str)

    if e_type == EntityType.ANSWER:
        entity = Answer()
        id_name = 'answer_option_id'
    elif e_type == EntityType.HINT:
        entity = Hint()
        e_type = EntityType.HINT
        id_name = 'hint_id'
    elif e_type == EntityType.MOVEMENT:
        entity = Movement()
        id_name = 'movement_id'
    else:
        return 'Bad Request', 400

    update_from_dict(entity, e_dict)
    e_id = g.container.add(e_type, entity)
    if e_type == EntityType.ANSWER:
        g.container.get(EntityType.QUESTION, question_id).answers.append(entity)
    elif e_type == EntityType.HINT:
        g.container.get(EntityType.QUESTION, question_id).hints.append(entity)
    else:  # entity is movement
        g.container.get(EntityType.QUESTION, question_id).movements.append(entity)

    return jsonify({id_name: e_id})


@api.route('/movement/<int:movement_id>/place', methods=['POST'])
def add_place(movement_id):
    place_dict = request.get_json(force=True)
    place = Place()
    update_from_dict(place, place_dict)
    place_id = g.container.add(EntityType.PLACE, place)
    g.container.get(EntityType.MOVEMENT, movement_id).place = place

    return jsonify({'place_id': place_id})


@api.route('/<e_type_str>/<int:e_id>', methods=['PUT'])
def update_entity(e_type_str, e_id):
    e_dict = request.get_json(force=True)
    e_type = EntityType.from_str(e_type_str)
    if e_type is None:
        return 'Bad Request', 400
    update_from_dict(g.container.get(e_type, e_id), e_dict)
    return '', 200


# TODO: delete entities


@api.route('/save/<int:quest_id>', methods=['POST'])
def save_quest(quest_id):
    # TODO: add remove method for container and refactor quest.to_db()
    #  g.container.get(EntityType.QUEST, quest_id).to_db()
    #  g.container.remove(EntityType.QUEST, quest_id)
    return '', 200


@api.route('/check/<int:q_id>', methods=['GET'])
def check(q_id):
    return jsonify(g.container.get(EntityType.QUEST, q_id).to_dict())
