from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from app.models import db, Card, Set, User, Sale, Trade, Log

from random import sample

from app.market import get_pack

user = Blueprint('user', __name__)

def get_card(id_str):
    return Card.query.filter_by(id_str=id_str).first()

def get_set(set):
    return Card.query.filter_by(set_name=set)

@user.route('/mycards')
@login_required
def mycards():
    c = current_user.cards
    return render_template('mycards.html', cards = c)

@user.route('/marketplace/cards')
@login_required
def cards():
    f = ['xy6-61','xy8-63','xy8-64','xy2-69','xy2-13','sm5-161','sm5-163','sm6-140','sm11-247','smp-SM210']
    f = [get_card(n) for n in f]
    featured = [f[:5],f[5:]]

    newest_set = 'Cosmic Eclipse'
    n = [c for c in get_set(newest_set)]
    print(get_set(newest_set))
    n = sample(n,10)
    new = [n[:5],n[5:]]

    p = Card.query.order_by(Card.num_sales)[:10]
    popular = [p[:5],p[5:]]

    return render_template('cards.html', featured=featured, new=new, popular=popular)

@user.route('/marketplace/packs')
@login_required
def packs():
    f = ['Legendary Collection','Legends Awakened','Legend Maker','Legendary Treasures','Shining Legends']
    featured = [Set.query.filter_by(name=c).first() for c in f]

    n = ['Cosmic Eclipse','Hidden Fates','Unified Minds','Unbroken Bonds','Detective Pikachu']
    new = [Set.query.filter_by(name=c).first() for c in n]

    p = ['Base', 'Ruby & Sapphire', 'Diamond & Pearl', 'Team Rocket', 'Sun & Moon']
    popular = [Set.query.filter_by(name=c).first() for c in p]

    return render_template('packs.html', featured=featured, new=new, popular=popular)

@user.route('/marketplace/trades')
@login_required
def trades():
    return render_template('trades.html', new=[], popular=[])

@user.route('/sell', methods=['GET','POST'])
@login_required
def sell():
    if 'card' in request.form.keys() and 'price' in request.form.keys():
        from app import app
        with app.app_context():
            Card.query.filter_by(id=request.form['card']).first().num_sales += 1
            sale = Sale(request.form['card'],request.form['price'],0,current_user.id)
            db.session.add(sale)
            db.session.commit()
        return redirect('mycards')
    return render_template('sales.html')