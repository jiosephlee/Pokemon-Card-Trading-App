from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

from app.models import Card, Set

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
    c = get_card('dp6-90')
    print(c)
    return render_template('mycards.html', card = c)

@user.route('/marketplace')
@login_required
def marketplace():
    f = ['xy6-61','xy8-63','xy8-64','xy2-69','xy2-13','sm5-161','sm5-163','sm6-140','sm11-247','smp-SM210']
    f = [get_card(n) for n in f]
    featured = [f[:5],f[5:]]
    newest_set = 'Cosmic Eclipse'
    n = [c for c in get_set(newest_set)]
    n = sample(n,10)
    new = [n[:5],n[5:]]

    p = ['Base', 'Team Rocket', 'Burning Shadows', 'Ancient Origins', 'Ruby & Sapphire']
    packs = [Set.query.filter_by(name=n).first() for n in p]
    # print(packs)
    # print("!!!!!!!!!!!!!!!!!")
    # for set in packs:
    #     print(set.logo)

    return render_template('marketplace.html', featured=featured, new=new, popular=packs)

@user.route('/marketplace/trade')
@login_required
def trade():
    return ''
