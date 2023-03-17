"""
Contains class of login user
"""

from flask_login import UserMixin


class Author(UserMixin):
    """
    Login user class. Needs to authenticate user with flask-login
    """
    class Type:
        AUTHOR = "author",
        MODERATOR = "moderator"

        @classmethod
        def get_type_by_id(cls, type: str) -> int:
            return cls.AUTHOR if type == cls.MODERATOR else cls.AUTHOR

    def __init__(self,
                 id: int,
                 email: int,
                 name: str,
                 password: str,
                 avatar_path: str,
                 status_name: str) -> None:
        """
        Init user with data from db
        :param author: dictionary with line from table authors
        """
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.avatar_path = avatar_path
        self.status_name = status_name

    @classmethod
    def load_from_dict(cls, author_info):
        return Author(author_info["author_id"],
                       author_info["email"], 
                       author_info["name"], 
                       author_info["password"], 
                       author_info["avatar_path"], 
                       cls.Type.get_type_by_id(author_info["status_id"]))

    def get_id(self):
        """
        Get this user id (from table authors)
        :return: this user id
        """
        return str(self.id)
