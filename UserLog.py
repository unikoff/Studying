class UserLog:
    def __init__(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def from_db(self, user, db):
        self.__user = db.select_user(user)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user['name']

    def get_psw(self):
        return self.__user['psw']

    def get_ava(self):
        return self.__user['ava']
