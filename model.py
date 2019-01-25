from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker
from webapp import db

class Users (db.Model):
    __tablename__ = "Users"
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(20), unique=True, nullable=False)
    email = db.Column('email', db.String(120), unique=True, nullable=False)
    password = db.Column('password', db.String(250), nullable=False)
    active = db.Column('active', db.Boolean, nullable=False, default=False)

