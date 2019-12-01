from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc

from app.models import db, Card, Set, User, Sale, Trade, Log, CardOwnership

from random import sample

from app.pack import get_pack

from app.forms import SearchForm

user = Blueprint('user', __name__)


def get_card(id_str):
    return Card.query.filter_by(id_str=id_str).first()


def get_set(set):
    return Card.query.filter_by(set_name=set)


def element_of(val, iterable):
    for item in iterable:
        if item.id == val:
            return True
    else:
        return False

def card_price(id):
    query = Sale.query.filter_by(card_id=id,status=0).order_by(Sale.cost).first()
    if query is None:
        return None
    else:
        return query.cost

# list of locations a user can be in
# ('location', 'currency short', 'symbol')
locations = [('United States', 'USD', '$'), ('Russia', 'RUB', '₽'),
             ('EU', 'EUR', '€'), ('Japan', 'JPY', '¥'), ('Korea', 'KRW', '₩')]


@user.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@user.route('/profile/mycards')
@login_required
def mycards():
    c = current_user.cards
    if len(c) > 0:
        a = [c[i * 5:(i + 1) * 5] for i in range((len(c) + 5 - 1) // 5)]
        while len(a[-1]) < 5:
            a[-1].append(0)
    else:
        a = []
        flash(
            'You currently do not own any cards. Buy cards or packs from the Marketplace!',
            'info')
    return render_template('mycards.html', title="My Cards", cards=a)


@user.route('/profile/mysales')
@login_required
def mysales():
    c = Sale.query.filter_by(user_id=current_user.id).all()
    if len(c) > 0:
        a = [c[i * 5:(i + 1) * 5] for i in range((len(c) + 5 - 1) // 5)]
        while len(a[-1]) < 5:
            a[-1].append(0)
        x = 0
        y = 0
        while x < 5:
            while y < 5:
                if (a[x][y] != 0):
                    a[x][y] = Card.query.filter_by(id=a[x][y].card_id).first()
                y += 1
            x += 1
    else:
        a = []
        flash(
            'None of your cards are up for sale. Sell cards in the Marketplace!',
            'info')

    return render_template('mycards.html', title="My Sales", cards=a)

@user.route('/profile/trades')
@login_required
def purchases():
    c = Trade.query.filter_by(user_id=current_user.id).filter_by(status=1).all()
    if len(c) > 0:
        a = [c[i * 5:(i + 1) * 5] for i in range((len(c) + 5 - 1) // 5)]
        while len(a[-1]) < 5:
            a[-1].append(0)
        x = 0
        y = 0
        while x < 5:
            while y < 5:
                if (a[x][y] != 0):
                    a[x][y] = Card.query.filter_by(id=a[x][y].card_id).first()
                y += 1
            x += 1
    else:
        a = []
        flash(
            'You have not bought any cards. Buy cards in the Marketplace!',
            'info')

    return render_template('mycards.html', title="Puchase History", cards=a)

@user.route('/profile/mytrades')
@login_required
def mytrades():
    c = Trade.query.filter_by(user_id=current_user.id).all()

    if len(c) == 0:
        flash(
            'You do not have any cards up for trade. Trade cards in the Marketplace!',
            'info')

    return render_template('mytrades.html', list=c)

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
    card = Card.query.filter_by(id=request.form['card']).first()
    s = Sale.query.filter_by(card_id=card.id).filter_by(status = 0).order_by(Sale.cost).first()
    #sales = Sale.query.filter_by(card_id=card.id).filter_by(status=0).all()
    #i = 0;
    #while i < len(sales):
    #    if sales[i].user_id == current_user.id:
    #        i += 1
    if s == None:
        flash('This card is no longer on sale',
              'danger')
        return redirect(url_for('user.cards'))
    if s.user_id == current_user.id:
        flash('You cannot buy your own card',
              'danger')
        return redirect(url_for('user.cards'))

    o = User.query.filter_by(id=s.user_id).first()
    if (float(s.cost) <= float(current_user.balance)):
        current_user.balance -= s.cost
        o.balance += s.cost
        current_user.cards.append(card)
        if sales[i].user_id != 4:
            o.balance += sales[i].cost
            o.cards.remove(card)
            sales[i].status = 1
        flash('You have brought ' + request.form['card'], 'success')
    else:
        flash('You do not enough money to buy ' + request.form['card'],
              'danger')
    db.session.commit()
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
    if (float(current_user.balance) >= 10):
        current_user.balance -= 10
        for card in cards:
            current_user.cards.append(card)
        flash('You have brought ' + request.form['set'], 'success')
    else:
        flash('You do not enough money to buy ' + request.form['set'],
              'danger')
    db.session.commit()
    return redirect(url_for('user.packs'))


@user.route('/marketplace/trades', methods=['GET', 'POST'])
@login_required
def trades():
    if 'trade' in request.form.keys():
        requested_card = Card.query.filter_by(
            id=request.form['requested_card']).first()
        given_card = Card.query.filter_by(
            id=request.form['given_card']).first()
        other_user = User.query.filter_by(id=request.form['user']).first()
        if element_of(int(requested_card.id), current_user.cards):
            flash('Trade completed!', 'success')
            current_user.cards.remove(requested_card)
            current_user.cards.append(given_card)
            other_user.cards.remove(given_card)
            other_user.cards.append(requested_card)
            Trade.query.filter_by(id=request.form['trade']).delete()
            db.session.commit()
        else:
            flash('You don\'t have that card!', 'danger')
    new = Trade.query.order_by(Trade.id.desc())
    new1 = [new[:2], new[2:4], new[4:6]]
    new2 = [new[6:8], new[8:10], new[10:12]]
    return render_template('trades.html', new_first=new1, new_second=new2)


@user.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    if len(current_user.cards) == 0:
        flash('You do not have any cards to trade!', 'danger')
        return redirect(url_for('user.trades'))
    if 'first_card' in request.form.keys(
    ) and 'second_card' in request.form.keys():
        flash('Your trade has been posted!', 'success')
        from app import app
        with app.app_context():
            t = Trade(request.form['second_card'], request.form['first_card'],current_user.id)
            db.session.add(t)
            db.session.commit()
            return redirect(url_for('user.trades'))
    return render_template('trade.html', query=Card.query)


@user.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if len(current_user.cards) == 0:
        flash('You do not have any cards to sell!', 'danger')
        return redirect(url_for('user.cards'))
    if 'card' in request.form.keys() and 'price' in request.form.keys():
        flash('Your sale has been posted!', 'success')
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

        sales = Sale.query.all()
        all_ids = set([i.card_id for i in sales])

        results = [i for i in results if i.id in all_ids]

        type_filter = form.types.data
        rarity_filter = form.rarities.data

        if len(type_filter) != 0:
            results = [
                i for i in filter(lambda x: x.type in type_filter, results)
            ]
        if len(rarity_filter) != 0:
            results = [
                i for i in filter(lambda x: x.rarity in rarity_filter, results)
            ]

        # cut results off
        results = results[:SEARCH_LIMIT]

        # pad results
        while len(results) % PER_ROW != 0:
            results.append(None)

        full_results = []

        print(full_results)

        for i in range(len(results) // PER_ROW):
            full_results.append(results[i * PER_ROW:(i + 1) * PER_ROW])

    form.rarities.data = []
    form.types.data = []

    return render_template('search.html',
                           form=form,
                           query=form.search.data,
                           limit=SEARCH_LIMIT,
                           results=full_results,
                           rarities=','.join(form.rarities.data),
                           types=','.join(form.types.data))


@user.route('/viewcard/<id>')
@login_required
def view_card(id):

    card = Card.query.get(id)

    return render_template('viewcard.html', card=card)
