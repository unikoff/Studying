import sqlite3
import os

from werkzeug.security import generate_password_hash, check_password_hash


class Db_plus():
    def __init__(self, db):
        self.db = db
        self.cur = db.cursor()

    def select_all(self):
        return self.cur.execute("SELECT * FROM user")

    def select_user(self, name):
        self.cur.execute(f"SELECT * FROM user WHERE name LIKE '{name}'")
        return self.cur.fetchone()

    def new_user(self, name, psw, ava='NULL'):
        self.cur.execute(f"SELECT COUNT() as `count` FROM user WHERE name LIKE '{name}'")
        if self.cur.fetchone()['count'] > 0:
            return False
        else:

            self.cur.execute(f"INSERT INTO user VALUES('{name}', '{generate_password_hash(psw)}', '{ava}')")
            if ava == 'NULL':
                with open('C:\\Users\\user\\PycharmProjects\\Studying\\static\\Image\\cat.png', mode='rb') as file:
                    ava = file.read()
                    binary = sqlite3.Binary(ava)
                    self.cur.execute("UPDATE user SET ava = ? WHERE name LIKE ?", (binary, name))
            self.db.commit()
            return True

    def authorization_user(self, name, psw):
        self.cur.execute(f"SELECT * FROM user WHERE name LIKE'{str(name)}'")
        res = self.cur.fetchone()
        if not (res is None):
            return check_password_hash(res['psw'], psw)

    def new_ava(self, ava, user):
        binary = sqlite3.Binary(ava)
        self.cur.execute("UPDATE user SET ava = ? WHERE name LIKE ?", (binary, user))
        self.db.commit()
        return True
