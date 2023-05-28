from flask import Flask, make_response, get_flashed_messages, \
    render_template, g, url_for, request, flash, redirect, \
    abort
from db_plus import *
import sqlite3
import os

"""CONFIG"""
DATABASE = 'first_p.db'
DEBUG = True
SECRET_KEY = 'fuio123wqrhouiuh'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'first_p.db')))

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


"""GLOBAL CONSTANT"""
db = None


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


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form['username'] == 'pp':
            flash('Удачно', category='up')
        else:
            flash('Не верно задано имя пользователя', category='down')
    return render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.cookies.get('log_name'):
        return redirect(url_for('profile', username=request.cookies.get('log_name')))
    elif request.method == 'POST' and request.form.get('user'):
        print(request.form.get('user'), request.form.get('password'))
        if db.authorization_user(request.form.get('user'), request.form.get('password')):
            res = make_response(redirect(url_for('profile', username=request.form.get('user'))))
            res.set_cookie('log_name', request.form.get('user'))
            return res
        else:
            flash('Ошибка', category='down')
    return render_template('login.html')


@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username):
    print(request.cookies, request.args)
    if request.cookies.get('log_name'):
        if request.args.get('but') and request.args.get('but') == 'delete':
            res = make_response(redirect(url_for('login')))
            res.set_cookie('log_name', max_age=0)
            return res
        elif request.cookies.get('log_name') == username:
            return render_template('profile.html', user=username)
    abort(401)


@app.errorhandler(404)
def danger(error):
    return render_template('error404.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['psw1'] == request.form['psw2'] and db.new_user(request.form['us'], request.form['psw1']):
            return redirect(url_for('login'))
        else:
            flash('Ошибка', category='down')
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
