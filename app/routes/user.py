from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import db, Card, Set, User, Sale, Trade, Log

from random import sample

from app.pack import get_pack

from app.forms import SearchForm

user = Blueprint('user', __name__)


def get_card(id_str):
    return Card.query.filter_by(id_str=id_str).first()


def get_set(set):
    return Card.query.filter_by(set_name=set)


# list of locations a user can be in
# ('location', 'currency')
locations = [('Protected Range', 'usd'), ('United States', 'usd'),
             ('Russia', 'ru')]


@user.route('/profile')
@login_required
def profile():
    c = current_user.cards
    if len(c) > 0:
        a = [c[i * 5:(i + 1) * 5] for i in range((len(c) + 5 - 1) // 5)]
        while len(a[-1]) < 5:
            a[-1].append(0)
    else:
        a = []
    return render_template('profile.html', cards=a)


@user.route('/marketplace/cards', methods=['GET'])
@login_required
def cards():
    f = [
        'xy6-61', 'xy8-63', 'xy8-64', 'xy2-69', 'xy2-13', 'sm5-161', 'sm5-163',
        'sm6-140', 'sm11-247', 'smp-SM210'
    ]
    f = [get_card(n) for n in f]
    featured = [f[:5], f[5:]]

    newest_set = 'Cosmic Eclipse'
    n = [c for c in get_set(newest_set)]
    n = sample(n, 10)
    new = [n[:5], n[5:]]

    p = Card.query.order_by(Card.num_sales)[:10]
    popular = [p[:5], p[5:]]

    return render_template('cards.html',
                           featured=featured,
                           new=new,
                           popular=popular)


@user.route('/marketplace/cards', methods=['POST'])
@login_required
def buyCards():
    c = User.query.filter_by(id=current_user.id).first()
    card = Card.query.filter_by(name=request.form['card']).first()
    c.cards.append(card)
    db.session.commit()
    flash('You have brought ' + request.form['card'], 'success')
    return redirect(url_for('user.cards'))


@user.route('/marketplace/packs', methods=['GET'])
@login_required
def packs():
    f = [
        'Legendary Collection', 'Legends Awakened', 'Legend Maker',
        'Legendary Treasures', 'Shining Legends'
    ]
    featured = [Set.query.filter_by(name=c).first() for c in f]

    n = [
        'Cosmic Eclipse', 'Hidden Fates', 'Unified Minds', 'Unbroken Bonds',
        'Detective Pikachu'
    ]
    new = [Set.query.filter_by(name=c).first() for c in n]

    p = [
        'Base', 'Ruby & Sapphire', 'Diamond & Pearl', 'Team Rocket',
        'Sun & Moon'
    ]
    popular = [Set.query.filter_by(name=c).first() for c in p]

    return render_template('packs.html',
                           featured=featured,
                           new=new,
                           popular=popular)


@user.route('/marketplace/packs', methods=['POST'])
@login_required
def buyPacks():
    cards = get_pack(request.form['set'])
    for card in cards:
        c = User.query.filter_by(id=current_user.id).first()
        c.cards.append(card)
    db.session.commit()
    flash('You have brought ' + request.form['set'], 'success')
    return redirect(url_for('user.packs'))


@user.route('/marketplace/trades')
@login_required
def trades():
    return render_template('trades.html', new=[], popular=[])


@user.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if len(current_user.cards) == 0:
        flash('You do not have any cards to sell!', 'danger')
        return redirect(url_for('user.cards'))
    if 'card' in request.form.keys() and 'price' in request.form.keys():
        from app import app
        with app.app_context():
            Card.query.filter_by(
                id=request.form['card']).first().num_sales += 1
            sale = Sale(request.form['card'], request.form['price'], 0,
                        current_user.id)
            db.session.add(sale)
            db.session.commit()
        return redirect(url_for('user.profile'))
    return render_template('sales.html')


@user.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    SEARCH_LIMIT = 100
    PER_ROW = 3

    form = SearchForm()

    full_results = None

    if form.validate_on_submit():
        results = Card.query.filter(
            Card.name.like('%{}%'.format(form.search.data))).all()
        results = results[:SEARCH_LIMIT]

        # pad results
        while len(results) % PER_ROW != 0:
            results.append(None)

        full_results = []

        for i in range(len(results) // PER_ROW):
            full_results.append(results[i * PER_ROW:(i + 1) * PER_ROW])
    return render_template('search.html',
                           form=form,
                           query=form.search.data,
                           limit=SEARCH_LIMIT,
                           results=full_results)
