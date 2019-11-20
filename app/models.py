from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_card_association = db.Table(
    'user_card_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)


class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    # relationships
    cards = db.relationship('Card', secondary=user_card_association)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 1000


class Card(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    picture_url = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)

    # relationships
    users = db.relationship('User', secondary=user_card_association)

    def __init__(self, name, picture_url, description, type):
        self.name = name
        self.picture_url = picture_url
        self.description = description
        self.type_id = type.id


class Trade(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    request_card_id = db.Column(db.ForeignKey('card.id'))
    given_card_id = db.Column(db.ForeignKey('card.id'))

    request_card = db.relationship('Card', foreign_keys=[request_card_id])
    given_card = db.relationship('Card', foreign_keys=[given_card_id])

    def __init__(self, request_id, given_id):
        self.request_id = request_id
        self.given_id = given_id
