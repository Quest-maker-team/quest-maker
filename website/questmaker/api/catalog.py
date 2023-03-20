from flask import Blueprint, jsonify, request
from questmaker.db import get_quest_from_catalog, get_tags as db_get_tags, \
    get_quest_tags, get_quest_rating, get_quests_from_catalog, get_quests_num

catalog_api = Blueprint("catalog_api", __name__)


def get_quest_dict(quest):
    quest = dict(quest)
    quest['rating'] = dict(get_quest_rating(quest['quest_id']))
    quest['tags'] = [tag['tag_name'] for tag in get_quest_tags(quest['quest_id'])]

    return quest


@catalog_api.route('/quests/<int:quest_id>', methods=['GET'])
def get_quest(quest_id):
    quest = get_quest_from_catalog(quest_id)
    if not quest:
        return "Not Found", 400

    return jsonify(get_quest_dict(quest))


@catalog_api.route('/quests', methods=['GET'])
def get_quests():
    title = request.args.get('title', default='', type=str)
    description = request.args.get('description', default='', type=str)
    limit = request.args.get('limit', default=100, type=int)
    offset = request.args.get('offset', default=0, type=int)
    sort_key = request.args.get('sort_by', default='id', type=str).lower()
    order = request.args.get('order_by', default='desc', type=str).lower()
    author = request.args.get('author', default=None, type=str)
    tags = request.args.getlist('tags', type=str)

    if limit < 0 or limit > 500 or offset < 0 or \
            sort_key not in ['id', 'rating', 'title'] or order not in ['asc', 'desc']:
        return 'Bad request', 400

    total, quests = get_quests_from_catalog(title, description, limit, offset, sort_key, order, author, tags)
    return {"quests": [get_quest_dict(quest) for quest in quests], "total": total}


@catalog_api.route('/tags', methods=['GET'])
def get_tags():
    return jsonify({"tags": [tag[0] for tag in db_get_tags()]})


@catalog_api.route('/quests/amount', methods=['GET'])
def get_quests_amount():
    return jsonify({'quests_amount': get_quests_num()})
