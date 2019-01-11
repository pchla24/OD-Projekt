from flask import Flask
from flask import session
from flask import request
from flask import Response
from flask import render_template
from flask import url_for
from flask import jsonify
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
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
