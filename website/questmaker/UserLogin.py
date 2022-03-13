"""
Contains class of login user
"""

from flask_login import UserMixin


class UserLogin(UserMixin):
    """
    Login user class. Needs to authenticate user with flask-login
    """
    def __init__(self, user):
        """
        Init user with data from db
        :param user: dictionary with line from table authors
        """
        self.user = user
        pass

    def get_id(self):
        """
        Get this user id (from table authors)
        :return: this user id
        """
        return str(self.user['id'])
