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
    msg = "Link aktywacyjny: " + activation_link

    send_mail('Aktywacja konta', msg, _email)

    return render_template('message.html', messageContent="Na podany adres została wysłana wiadomość zawierająca link aktywacyjny. Zalogowanie będzie możliwe dopiero po aktywowaniu konta.")

"""
@app.route('/activateAccount/<string:activation_token>')
def activateAccount(activation_token):
    return redirect('/userActivated')
"""

"""
@app.route('/userActivated')
def userActivated():
    return render_template('userActivated.html')
"""

"""
@app.route('/forgotPassSendEmail', methods=['POST'])
def forgotPassSendEmail():
    return render_template('message.html', messageContent="Na poday adres została wysłana wiadomość zawierająca link do zmiany hasła.")
"""
"""
@app.route('/retrievePassword/<string:retrieve_token>')
def retrievePassword(retrieve_token):
    return render_template('retrievePassForm.html')
"""
"""
@app.route('/changeForgottenPass', methods=['POST'])
def changeForgottenPass():
    return render_template('message.html', messageContent="Hasło zostało zmienione")
"""
"""
@app.route('/changePasswordForm')
def changePasswordForm():
    return render_template('changePasswordForm.html')
"""
"""
@app.route('/changePassword', methods=['POST'])
def changePassword():
    return render_template('loggedMessage.html', messageContent="Hasło zostało zmienione")
"""



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