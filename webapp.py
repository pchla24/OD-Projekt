from flask import Flask
from flask import session
from flask import request
from flask import Response
from flask import render_template
from flask import url_for
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from os import environ as env
from os.path import expanduser
from flask import redirect
import jwt
import uuid
import datetime
from functools import wraps
# from six.moves.urllib.parse import urlencode
from werkzeug.utils import secure_filename
import hashlib
import binascii
import re
from flask_mail import Mail, Message
import random
import time

app = Flask(__name__)

#app.config['SESSION_COOKIE_SECURE'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

app.config.from_pyfile('sec.cfg')

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///od.db'
db = SQLAlchemy(app)

import model


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    _username = request.form['login']
    _email = request.form['email']
    _password = request.form['password']

    _hashedPassword = hash_password(_password)

    delay()

    username_taken = model.Users.query.filter_by(username=_username).first()
    if username_taken:
      return render_template('message.html', messageContent="Nazwa użytkownika jest już zajęta")

    emial_taken = model.Users.query.filter_by(email = _email).first()
    if emial_taken:
      return render_template('message.html', messageContent="Adres email jest już w użyciu")

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", _email):
      return render_template('message.html', messageContent="Adres email jest niepoprawny")

    new_user = model.Users(username=_username, email=_email, password=_hashedPassword)
    db.session.add(new_user)
    db.session.commit()

    activation_token_parts = {
			'username': _username,
			'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
		}

    activation_token = str(jwt.encode(activation_token_parts,app.config['SECRET_KEY']))[2:-1]
    activation_link = 'http://127.0.0.1:5000/activateAccount/' + activation_token
    msg = "Link aktywacyjny (ważny przez 5 minut): " + activation_link

    send_mail('Aktywacja konta', msg, _email)

    return render_template('message.html', messageContent="Na podany adres została wysłana wiadomość zawierająca link aktywacyjny. Zalogowanie będzie możliwe dopiero po aktywowaniu konta.")


@app.route('/activateAccount/<string:activation_token>')
def activateAccount(activation_token):
    activation_token_parts = {}
    try:
      activation_token_parts = jwt.decode(activation_token, app.config['SECRET_KEY'])
    except jwt.ExpiredSignatureError:
      return render_template('message.html', messageContent="Termin ważności linku wygasł")
    _username = activation_token_parts['username']
    user_to_activate = model.Users.query.filter_by(username=_username).first()
    user_to_activate.active = True
    db.session.commit()

    return redirect('/userActivated')


@app.route('/userActivated')
def userActivated():
    return render_template('userActivated.html')


@app.route('/signIn', methods=['POST'])
def signIn():
    _username = request.form['login']
    _password = request.form['password']

    user_to_signin = model.Users.query.filter_by(username=_username).first()

    delay()

    if user_to_signin:
      if verify_password(user_to_signin.password, _password) and user_to_signin.active:
        session['user'] = _username
        return redirect('/userHome')

    return render_template('message.html', messageContent="Niepoprawna nazwa użytkownika lub hasło lub konto nie zostało aktywowane")


@app.route('/userHome')
def userHome():
    if session.get('user'):
      username = session['user']
      return render_template('userHome.html', username=username)
    else:
      return redirect('/')


@app.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassForm.html')


@app.route('/forgotPassSendEmail', methods=['POST'])
def forgotPassSendEmail():
    _email = request.form['email']

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", _email):
      return render_template('message.html', messageContent="Podany adres email jest niepoprawny")

    user_to_retrieve = model.Users.query.filter_by(email=_email).first()
    if user_to_retrieve:
      fgPass_token_parts = {
        'email': _email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
      }

      fgPass_token = str(jwt.encode(fgPass_token_parts,app.config['SECRET_KEY']))[2:-1]
      fgPass_link = 'http://127.0.0.1:5000/retrievePassword/' + fgPass_token
      msg = "Link do zmiany hasła (ważny przez 5 minut): " + fgPass_link

      send_mail('Zmiana hasła', msg, _email)

      return render_template('message.html', messageContent="Na poday adres została wysłana wiadomość zawierająca link do zmiany hasła.")

    else:
      return render_template('message.html', messageContent="Użytkownik o podanym adresie email nie istnieje")


@app.route('/retrievePassword/<string:retrieve_token>')
def retrievePassword(retrieve_token):
    fgPass_token_parts = {}
    try:
      fgPass_token_parts = jwt.decode(retrieve_token, app.config['SECRET_KEY'])
    except jwt.ExpiredSignatureError:
      return render_template('message.html', messageContent="Termin ważności linku wygasł")

    _email = fgPass_token_parts['email']

    return render_template('retrievePassForm.html', email=_email)


@app.route('/changeForgottenPass', methods=['POST'])
def changeForgottenPass():
    _password = request.form['password']
    _email = request.form['email']

    _hashedPassword = hash_password(_password)

    delay()

    user_to_retrieve = model.Users.query.filter_by(email=_email).first()
    if user_to_retrieve:
      user_to_retrieve.password = _hashedPassword
      db.session.commit()
      return render_template('message.html', messageContent="Hasło zostało zmienione")
    else:
      return render_template('message.html', messageContent="Błąd - parametr email został zmieniony, użytkownik o podanym adresie email nie istnieje")


@app.route('/changePasswordForm')
def changePasswordForm():
    return render_template('changePasswordForm.html')


@app.route('/changePassword', methods=['POST'])
def changePassword():
    _oldPassword = request.form['oldPassword']
    _newPassword = request.form['password']
    _username = session['user']

    user = model.Users.query.filter_by(username=_username).first()

    if verify_password(user.password, _oldPassword):
      _hashedNewPassword = hash_password(_newPassword)

      delay()

      user.password = _hashedNewPassword
      db.session.commit()
  
      return render_template('loggedMessage.html', messageContent="Hasło zostało zmienione")

    else:
      return render_template('loggedMessage.html', messageContent="Hasło nie zostało zmienione z powodu podania niepoprawnego aktualnego hasła")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def send_mail(title, message, receiver):
    msg = Message(title, sender='ochronadanychjs@gmail.com', recipients=[receiver])
    msg.body = message
    mail.send(msg)


def delay():
    delayTime = random.uniform(0,1)
    time.sleep(delayTime)