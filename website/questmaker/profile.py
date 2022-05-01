"""
Contains blueprint for profile page and related functionality
"""

from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .db import get_quests_by_author_id
import operator


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
    if not quest['published']:
        return 'Не опубликован', 'secondary'
    elif quest['hidden']:
        return 'Ждет одобрения', 'warning'
    elif (quest['time_open'] == None or quest['time_open'] < datetime.now())\
            and (quest['time_close'] == None or quest['time_close'] > datetime.now()):
        return 'Активен', 'info'
    else:
        return 'Неактивен', 'light'


@prof.route('/profile_catalog')
@login_required
def catalog():
    """
    Personal catalog page
    :return: personal catalog page
    """
    quests = get_quests_by_author_id(current_user.author['author_id'])
    catalog = []

    for q in quests:
        c = {}
        c['keyword'] = q['keyword']
        c['title'] = q['title']
        if q['password'] != None:
            c['type'] = 'Приватный'
        else:
            c['type'] = 'Публичный'
        c['state'], c['color'] = choose_state(q)
        catalog.append(c)
    
    catalog.sort(key=operator.itemgetter('title'))

    return render_template('profile_catalog.html', user=current_user, quests=catalog)