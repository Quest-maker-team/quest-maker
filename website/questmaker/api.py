from flask import Blueprint, jsonify
from . import quest

api = Blueprint('api', __name__)


@api.route('/quest/<quest_id>', methods=['GET'])
def get_quest(quest_id):
    return jsonify(quest.Quest().from_db(quest_id).to_dict())
