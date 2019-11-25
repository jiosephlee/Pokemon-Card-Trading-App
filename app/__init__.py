import os

from flask import Flask, render_template, request
from flask_login import LoginManager, login_required

from app.forms import SignUpForm, LogInForm
from app.models import db, User, Card, Set
from app.routes.auth import auth
from app.routes.user import user

from app.ip_address import get_location

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

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def make_global_variables():
    ip = request.remote_addr

    if request.headers.getlist('X-Forwarded-For'):
        ip = request.headers.getlist('X-Forwarded-For')[0]
    return dict(ip_location=get_location(ip))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
