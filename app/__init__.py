import os

from flask import Flask, render_template
from flask_login import LoginManager, login_required

from app.forms import SignUpForm, LogInForm
from app.models import db, User
from app.routes.auth import auth
from app.routes.user import user

app = Flask(__name__)

# app configurations
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['USE_SESSION_FOR_NEXT'] = True

# start database
db.init_app(app)

with app.app_context():
    db.create_all()

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
