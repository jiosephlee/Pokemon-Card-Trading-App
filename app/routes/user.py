from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

from app.models import Card

user = Blueprint('user', __name__)

def get_card(id_str):
    return Card.query.filter_by(id_str=id_str).first()

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
    return render_template('mycards.html')
    # cards = current_user.cards)


@user.route('/marketplace')
@login_required
def marketplace():
    featured = ['xy6-61','xy8-63','xy8-64','xy2-69','xy2-13']
    featured = [get_card(n) for n in featured]
    return render_template('marketplace.html', featured=featured, new=[], popular=[], value=[])
