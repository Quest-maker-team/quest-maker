"""
Contains blueprint for profile page and related functionality
"""

from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .db import get_drafts_by_author_id, get_quests_by_author_id

import pickle


prof = Blueprint('profile', __name__)


@prof.route('/profile')
@login_required
def profile():
    """
    Main profile page
    :return: main profile page
    """
    return render_template('profile.html', user=current_user)


def choose_state(quest):
    """
    Evaluate the status of the quest
    :param quest: quest whose state needs to be assessed
    :return: quest state and bootstrap color name for catalog row
    """
    if quest['hidden']:
        return 'Ждет одобрения', 'danger'
    elif (quest['time_open'] == None or quest['time_open'] < datetime.now())\
            and (quest['time_close'] == None or quest['time_close'] > datetime.now()):
        return 'Активен', 'info'
    else:
        return 'Неактивен', 'warning'


@prof.route('/profile_catalog')
@login_required
def catalog():
    """
    Personal catalog page
    :return: personal catalog page
    """
    drafts = get_drafts_by_author_id(current_user.author['author_id'])
    cleans = get_quests_by_author_id(current_user.author['author_id'])
    quests = []

    for d in drafts:
        q = {}
        q['id'] = d['draft_id']
        q['title'] = pickle.loads(bytes(d['container'])).quest.title
        q['type'] = 'Черновик'
        q['state'] = 'Черновик'
        q['color'] = 'secondary'
        quests.append(q)

    for c in cleans:
        q = {}
        q['id'] = c['quest_id']
        q['title'] = c['title']
        if c['password'] != None:
            q['type'] = 'Публичный'
        else:
            q['type'] = 'Приватный'
        q['state'], q['color'] = choose_state(c)
        quests.append(q)

    return render_template('profile_catalog.html', user=current_user, quests=quests)