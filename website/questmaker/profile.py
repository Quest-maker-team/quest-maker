from flask import Blueprint, render_template
from flask_login import login_required, current_user

prof = Blueprint('profile', __name__)


@prof.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.user)
