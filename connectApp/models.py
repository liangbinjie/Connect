from typing import NamedTuple
from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(40))
    pfp = db.Column(db.LargeBinary())

    links = db.relationship('Links', backref="owner")



class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    
    
