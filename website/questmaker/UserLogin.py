from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self, user):
        self.user = user
        pass

    def get_id(self):
        return str(self.user['id'])
