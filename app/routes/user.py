from flask import Blueprint
from flask import render_template
from flask_login import login_required

user = Blueprint('user', __name__)


@user.route('/home')
@login_required
def home():
    return render_template('home.html')
