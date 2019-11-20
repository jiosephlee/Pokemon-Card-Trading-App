from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_card_association = db.Table(
    'user_card_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)

card_trade_association = db.Table(
    'card_trade_association',
    db.Column('trade_id', db.Integer, db.ForeignKey('trade.id')),
    db.Column('request_card_id', db.Integer, db.ForeignKey('card.id')),
    db.Column('given_card_id', db.Integer, db.ForeignKey('card.id'))
)

card_sale_association = db.Table(
    'card_sale_association',
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)

type_card_association = db.Table(
    'type_card_association',
    db.Column('type_id', db.Integer, db.ForeignKey('type.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.type_id'))
)

card_move_association = db.Table(
    'card_move_association',
    db.Column('card_id', db.Integer, db.ForeignKey('type.id')),
    db.Column('move_id', db.Integer, db.ForeignKey('move.id'))
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
    type_id = db.Column(db.ForeignKey('type.id'))

    # relationships
    users = db.relationship('User', secondary=user_card_association)
    trades = db.relationship('Trade', secondary=card_trade_association)
    sales = db.relationship('Sale', secondary=card_sale_association)
    type = db.relationship('Type', foreign_keys=[type_id])
    moves = db.relationship('Move', secondary=card_move_association)

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


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)

    cards = db.relationship('Card', secondary=type_card_association)

    def __init__(self, type):
        self.type = type


class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.ForeignKey('card.id'))
    description = db.Column(db.Text, nullable=False)

    cards = db.relationship('Card')

    def __init__(self, card, description):
        self.card = card
        self.description = description


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.ForeignKey('user.id'))
    second_user_id = db.Column(db.ForeignKey('user.id'))

    first_user = db.relationship('User', foreign_keys=[first_user_id])
    second_user = db.relationship('User', foreign_keys=[second_user_id])

    def __init__(self, first_user, second_user):
        self.first_user_id = first_user
        self.second_user_id = second_user
