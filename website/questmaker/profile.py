"""
Contains blueprint for profile page and related functionality
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

prof = Blueprint('profile', __name__)


@prof.route('/profile')
@login_required
def profile():
    """
    Main profile page
    :return: main profile page
    """
    return render_template('profile.html', user=current_user)
