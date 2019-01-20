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
# import jwt
import uuid
import datetime
from functools import wraps
# from six.moves.urllib.parse import urlencode
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_pyfile('sec.cfg')
#app.config['SESSION_COOKIE_SECURE'] = True

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

"""
@app.route('/signUp')
def signUp():
    return render_template('message.html', messageContent="Na podany adres została wysłana wiadomość zawierająca link aktywacyjny. Zalogowanie będzie możliwe dopiero po aktywowaniu konta.")
"""
"""
@app.route('/userActivated')
def userActivated():
    return render_template('userActivated.html')
"""
"""
@app.route('/activateAccount/<string:activation_token>')
def activateAccount(activation_token):
    return redirect('/userActivated')
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

