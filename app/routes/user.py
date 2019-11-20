from flask import Blueprint
from flask import render_template
from flask_login import login_required

user = Blueprint('user', __name__)


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
    return render_template('mycards.html')
                            #cards = allcards)

@user.route('/marketplace')
@login_required
def marketplace():
    return render_template('marketplace.html')
