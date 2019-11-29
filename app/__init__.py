import os

from flask import Flask, render_template, request, session
from flask_login import LoginManager, login_required

from app.forms import SignUpForm, LogInForm, get_type_options, get_rarity_options
from app.models import db, User, Card, Set, Sale, ExchangeRate, Trade, CardOwnership
from app.routes.auth import auth
from app.routes.user import user, locations
from app.ip_address import get_location
from app.exchange_rates import get_exhange_rate

from random import randint

import urllib.request as urllib
import json

app = Flask(__name__)

DEBUG = True

# app configurations
app.config['SECRET_KEY'] = ('very secret key wow' if DEBUG else os.urandom(64))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['USE_SESSION_FOR_NEXT'] = True

# start database
db.init_app(app)

with app.app_context():
    db.create_all()
    '''
    x = 1
    while (x < 13):
        url = "https://api.pokemontcg.io/v1/cards?pageSize=1000&page=" + str(x)
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        req = urllib.Request(url, headers=hdr)
        data = json.loads(urllib.urlopen(req).read())

        i = 0
        if (x != 12):
            end = 1000
        else:
            end = 901
        while (i < end):
            name = data['cards'][i]['name']
            id_str = data['cards'][i]['id']
            image = data['cards'][i]['imageUrl']
            hires = data['cards'][i]['imageUrlHiRes']
            card_set = data['cards'][i]['set']
            series = data['cards'][i]['series']
            if ('rarity' in data['cards'][i]):
                rarity = data['cards'][i]['rarity']
            else:
                rarity = None
            if (data['cards'][i]['supertype'] == 'Pokémon'):
                types = ''
                for type in data['cards'][i]['types']:
                    types += type+','
                types = types[:-1]
            else:
                types = None
            if ('subtype' in data['cards'][i]):
                subtype = data['cards'][i]['subtype']
            else:
                subtype = None
            supertype = data['cards'][i]['supertype']
            card = Card(name,id_str,image,hires,types,card_set,series,subtype,supertype,rarity)
            db.session.add(card)
            i += 1
        x += 1
    db.session.commit()
    '''
    '''
    url = "https://api.pokemontcg.io/v1/sets"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.Request(url, headers=hdr)
    data = json.loads(urllib.urlopen(req).read())

    for i in range(109):
        name = data['sets'][i]['name']
        logo = data['sets'][i]['logoUrl']
        set = Set(name,logo)
        db.session.add(set)

    db.session.commit()
    '''
    '''
    for i in range(30):
        given = randint(1,11901)
        request = randint(1,11901)
        trade = Trade(request,given,4)
        db.session.add(trade)
    db.session.commit()
    '''

    for card in Card.query.all():
        price = 5
        if(card.type == "Uncommon"):
            price = 10
        elif (card.type == "Rare"):
            price = 15;
        elif (card.type == "Shining"):
            price = 20;
        elif ("Rare" in card.type):
            price = 25;
        else:
            price = 30;
        sale = Sale(card.id,price,0,4)
        db.session.add(sale)
    db.session.commit()

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'


def get_card_id(id):
    return Card.query.filter_by(id=id).first()


app.jinja_env.globals.update(get_card_id=get_card_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.before_request
def before_request():
    if 'user_currency' not in session:
        session['user_currency'] = 'USD'


@app.context_processor
def make_global_variables():

    ip = request.remote_addr

    if request.headers.getlist('X-Forwarded-For'):
        ip = request.headers.getlist('X-Forwarded-For')[0]

    # we need to update the list of the locations so the first one is the one that the user is supposedly in
    current_currency = session['user_currency']
    current_location = list(
        filter(lambda x: x[1] == current_currency, locations))[0]
    updated_locations = locations[:]
    updated_locations.remove(current_location)
    updated_locations = [current_location] + updated_locations

    return dict(ip_location=get_location(ip), locations=updated_locations)


# this makes a filter that we use any time we want to display a currency so it's displayed as whatever the user wants
@app.template_filter('change_currency')
def change_currency(text):
    current_currency = session['user_currency']
    # get the symbol
    symbol = list(filter(lambda x: x[1] == current_currency, locations))[0][2]
    # get the exchange rate
    rate = get_exhange_rate(current_currency)
    num = int(text)

    # currency-number is empty because JS fills it in for us
    return """
    <span class="currency-original" style="display: none;">%s</span>
    <span class="currency-symbol">%s</span>
    <span class="currency-number"></span>
""" % (text, symbol)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/update_user_currency/<currency>', methods=['POST'])
def update_user_currency(currency):
    session['user_currency'] = currency
    rate = get_exhange_rate(currency)
    symbol = list(filter(lambda x: x[1] == currency, locations))[0][2]
    ret = {'rate': rate, 'symbol': symbol}

    return json.dumps(ret)


from app.forms import get_rarity_options


@app.route('/test')
def test():

    return str(get_type_options())


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
