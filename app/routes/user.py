from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

from app.models import Card

from random import sample

user = Blueprint('user', __name__)

def get_card(id_str):
    return Card.query.filter_by(id_str=id_str).first()

def get_set(set):
    return Card.query.filter_by(set_name=set)

@user.route('/mycards')
@login_required
def mycards():
    # command='''
    #     SELECT
    #         card_id
    #     FROM
    #         card_ownership
    #     WHERE
    #         user_id == user
    #     '''
    # allcards = c.fetchall()
    # allcards = card_ownership.query.filter_by(user_id == user).all()
    c = get_card('dp6-90')
    print(c)
    return render_template('mycards.html', card = c)
    # cards = current_user.cards)

@user.route('/marketplace/cards')
@login_required
def cards():
    f = ['xy6-61','xy8-63','xy8-64','xy2-69','xy2-13','sm5-161','sm5-163','sm6-140','sm11-247','smp-SM210']
    f = [get_card(n) for n in f]
    featured = [f[:5],f[5:]]
    newest_set = 'Cosmic Eclipse'
    n = [c for c in get_set(newest_set)]
    n = sample(n,10)
    new = [n[:5],n[5:]]
    p = Card.query.order_by(Card.num_sales)[:10]
    popular = [p[:5],p[5:]]
    return render_template('cards.html', featured=featured, new=new, popular=popular)

@user.route('/marketplace/packs')
@login_required
def packs():
    return ''

@user.route('/marketplace/trades')
@login_required
def trades():
    return ''
