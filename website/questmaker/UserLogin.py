"""
Contains class of login user
"""

from flask_login import UserMixin


class AuthorLogin(UserMixin):
    """
    Login user class. Needs to authenticate user with flask-login
    """
    def __init__(self, author):
        """
        Init user with data from db
        :param author: dictionary with line from table authors
        """
        self.author = author
        pass

    def get_id(self):
        """
        Get this user id (from table authors)
        :return: this user id
        """
        return str(self.author['author_id'])
