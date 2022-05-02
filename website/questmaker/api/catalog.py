from flask import Blueprint

catalog_api = Blueprint("catalog_api", __name__)


@catalog_api.route('/quests/<int:quest_id>', methods=['GET'])
def get_quest():
    pass


@catalog_api.route('/quests', methods=['GET'])
def get_quests():
    pass


@catalog_api.route('/tags', methods=['GET'])
def get_tags():
    pass
