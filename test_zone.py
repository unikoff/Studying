from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import sqlite3
import os
from re import findall
app = Flask(__name__)
app.config['SECRET_KEY'] = 'loxasfasfasf213123'

menu = [{'name': 'Главная', 'url': '/'},
        {'name': 'Дополнительно', 'url': 'about'},
        {'name': 'Контакты', 'url': 'contact'}]


@app.route("/profile/<user>")
def profile(user):
    if 'userlogget' not in session or session['userlogget'] != user:
        abort(401)
    return render_template('profile.html', menu=menu, user=user)


@app.route("/login", methods=['POST', "GET"])
def login():
    if 'userlogget' in session:
        return redirect(url_for('profile', user=session['userlogget']))
    elif request.method == 'POST':
        session['userlogget'] = request.form['us']
        return redirect(url_for('profile', user=session['userlogget']))
    return render_template('login.html', menu=menu, title='Авторизация')


@app.route("/")
def index():
    return render_template('index.html', title='Главная')


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if findall(r".+@\w+\.\w+", request.form["email"])[0] == request.form["email"]:
            flash('Удачно!', category='up')
        else:
            flash('Неудачно!', category='down')
        print(request.form)
    return render_template('contact.html', title='Контакты')


@app.route("/about")
def about():
    return render_template('about.html', menu=menu, title='Дополнительная Информация')


@app.errorhandler(404)
def er(error):
    return render_template('error404.html', title='Ошибка')


if __name__ =='__main__':
    app.run(debug=True)