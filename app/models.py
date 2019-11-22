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
    name = db.Column(db.String(80), nullable=False)
    id_str = db.Column(db.String(80), nullable=False)
    image_small = db.Column(db.String(80), nullable=False)
    image_hires = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=True)
    set_name = db.Column(db.String(80), nullable=False)
    series = db.Column(db.String(80), nullable=False)
    subtype = db.Column(db.String(80))
    supertype = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.String(80))

    # relationships
    users = db.relationship('User', secondary=user_card_association)

    def __init__(self, name, id_str, image_small, image_hires, type, set_name, series, subtype, supertype, rarity):
        self.name = name
        self.id_str = id_str
        self.image_small = image_small
        self.image_hires = image_hires
        self.type = type
        self.set_name = set_name
        self.series = series
        self.subtype = subtype
        self.supertype = supertype
        self.rarity = rarity


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    logo = db.Column(db.String(80), nullable=False)

    def __init__(self, name, logo):
        self.name = name
        self.logo = logo


class Trade(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    request_card_id = db.Column(db.ForeignKey('card.id'))
    given_card_id = db.Column(db.ForeignKey('card.id'))

    # relationships
    request_card = db.relationship('Card', foreign_keys=[request_card_id])
    given_card = db.relationship('Card', foreign_keys=[given_card_id])

    def __init__(self, request_id, given_id):
        self.request_id = request_id
        self.given_id = given_id


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.ForeignKey('card.id'))
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    card = db.relationship('Card')

    def __init__(self, card_id, cost, status):
        self.card_id = card_id
        self.cost = cost
        self.status = status


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.ForeignKey('user.id'))
    second_user_id = db.Column(db.ForeignKey('user.id'))

    first_user = db.relationship('User', foreign_keys=[first_user_id])
    second_user = db.relationship('User', foreign_keys=[second_user_id])

    def __init__(self, first_user, second_user):
        self.first_user_id = first_user
        self.second_user_id = second_user
