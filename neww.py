from flask import Flask, make_response, render_template, g, url_for, request, \
    flash, redirect, abort
from Admin.admin import admin

from db_plus import *
import sqlite3
import os

from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from UserLog import *

from forms import *

"""CONFIG"""
DATABASE = 'first_p.db'
DEBUG = True
SECRET_KEY = 'fuio123wqrhouiuh'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'first_p.db')))
UPLOAD_FOLDER = 'C:\\Users\\user\\PycharmProjects\\Studying\\static\\image'
app.register_blueprint(admin, url_prefix='/admin')

db = None

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа требуется регистрация'
login_manager.login_message_category = 'down'

"""DATABASE"""


def connect_db():
    con_db = sqlite3.connect(app.config['DATABASE'])
    con_db.row_factory = sqlite3.Row
    return con_db


def create_db():
    db = connect_db()
    with open('template_db.sql', mode='r') as file_t:
        db.cursor().executescript(file_t.read())
    db.commit()
    db.close()


def get_db():
    """Проверка на соединение с бд"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Проверка на соединение с бд"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@login_manager.user_loader
def load_user(user):
    return UserLog().from_db(user, db)


@app.before_request
def bef_req():
    global db
    db = get_db()
    db = Db_plus(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    elif form.validate_on_submit():
        if db.authorization_user(form.name.data, form.psw.data):
            user = UserLog().create(db.select_user(form.name.data))
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Ошибка', 'down')
    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = Profile()
    if form.validate_on_submit():
        if form.but_del.data:
            return redirect('/logout')
        elif form.ava.data:
            file = form.ava.data
            db.new_ava(file.read(), current_user.get_id())
    return render_template('profile.html', form=form)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    img = current_user.get_ava()
    res = make_response(img)
    res.content_type = 'image/png'
    return res


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Выход выполнен', 'up')
    return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = Registration()
    if form.validate_on_submit():
        if form.psw1.data == form.psw2.data and db.new_user(form.name.data, form.psw1.data):
            user = UserLog().create(db.select_user(form.name.data))
            login_user(user)
            return redirect(url_for('login'))
        else:
            flash('Ошибка', category='down')
    return render_template('registration.html', form=form)


@app.errorhandler(404)
def danger(error):
    return render_template('error404.html')


if __name__ == '__main__':
    app.run()
