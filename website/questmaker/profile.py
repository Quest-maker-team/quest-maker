from flask import Blueprint, render_template

prof = Blueprint('profile', __name__)


@prof.route('/profile')
def profile():
    return render_template('profile.html')
