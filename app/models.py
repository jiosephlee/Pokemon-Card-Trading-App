from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class CardOwnership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))

    user = db.relationship('User', backref='ownership')
    card = db.relationship('Card', backref='ownership')

    def __init__(self, user_id, card_id):
        self.user_id = user_id
        self.card_id = card_id


class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    cards = association_proxy('ownership',
                              'card',
                              creator=lambda c: CardOwnership(id, c.id))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 1000


class Card(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    id_str = db.Column(db.String(80), unique=True, nullable=False)
    image_small = db.Column(db.String(80), nullable=False)
    image_hires = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=True)
    set_name = db.Column(db.String(80), nullable=False)
    series = db.Column(db.String(80), nullable=False)
    subtype = db.Column(db.String(80))
    supertype = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.String(80))
    num_sales = db.Column(db.Integer, nullable=False)

    users = association_proxy('ownership',
                              'user',
                              creator=lambda u: CardOwnership(u.id, id))

    def __init__(self, name, id_str, image_small, image_hires, type, set_name,
                 series, subtype, supertype, rarity):
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
        self.num_sales = 0


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
    user_id = db.Column(db.ForeignKey('user.id'))

    # relationships
    request_card = db.relationship('Card', foreign_keys=[request_card_id])
    given_card = db.relationship('Card', foreign_keys=[given_card_id])
    user = db.relationship('User')

    def __init__(self, request_id, given_id, user_id):
        self.request_card_id = request_id
        self.given_card_id = given_id
        self.user_id = user_id


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.ForeignKey('card.id'))
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    buyer_id = db.Column(db.ForeignKey('user.id'))

    card = db.relationship('Card')

    def __init__(self, card_id, cost, status, user_id, buyer_id):
        self.card_id = card_id
        self.cost = cost
        self.status = status
        self.user_id = user_id
        self.buyer_id = buyer_id


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.ForeignKey('user.id'))
    second_user_id = db.Column(db.ForeignKey('user.id'))

    first_user = db.relationship('User', foreign_keys=[first_user_id])
    second_user = db.relationship('User', foreign_keys=[second_user_id])

    def __init__(self, first_user, second_user):
        self.first_user_id = first_user
        self.second_user_id = second_user


# this table is used for looking up IP address locations
# we use it because we don't want to spam the IP Address API too much
class IPAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_str = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)

    def __init__(self, ip_str, location):
        self.ip_str = ip_str
        self.location = location


# we use this class for storing exchange rates
# we only store the exchange rate to USD since that's the unit the database uses
class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(80), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __init__(self, currency, rate, timestamp):
        self.currency = currency
        self.rate = rate
        self.timestamp = timestamp
