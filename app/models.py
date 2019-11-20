from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    # relationships

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 1000


class Cards(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    picture_url = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)

    # relationships

    def __init__(self, name, picture_url, description, type):
        self.name = name
        self.picture_url = picture_url
        self.description = description
        self.type_id = type.id

class Trades(db.Model):
    #columns
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, nullable=False)
    given_id = db.Column(db.Integer, nullable=False)

    def __init__(self,request_id,given_id):
        self.request_id = request_id
        self.given_id = given_idg
