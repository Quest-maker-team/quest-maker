from flask import Blueprint
from flask_login import login_required, current_user
from questmaker.db import get_quest, remove_quest

personal_catalog_api = Blueprint("personal_catalog", __name__)


@personal_catalog_api.route('/quest/<int:quest_id>', methods=['DELETE'])
@login_required
def remove_quest(quest_id):
    if get_quest['author_id'] != current_user.author['author_id']:
        return 'This is not your quest', 403
    return ('', 200) if remove_quest(quest_id) else ('Wrong id', 400)
