from flask import Blueprint, session
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from app.forms import SignUpForm, LogInForm
from app.models import db, User

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_up_form = SignUpForm()

    if sign_up_form.validate_on_submit():
        # we just need to check that no accounts exist with the same username
        if User.query.filter_by(username=sign_up_form.username.data).first() is not None:
            flash('Username taken!', 'danger')
        else:
            # create the account
            new_account = User(sign_up_form.username.data, sign_up_form.password.data)
            db.session.add(new_account)
            db.session.commit()

            flash('Account Created!', 'success')

    return render_template('signup.html', form=sign_up_form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    log_in_form = LogInForm()

    if log_in_form.validate_on_submit():
        to_validate = User.query.filter_by(username=log_in_form.username.data).first()

        if to_validate is None or to_validate.password != log_in_form.password.data:
            flash('Incorrect username or password!', 'danger')
        else:
            login_user(to_validate)

            if 'next' in session:
                return redirect(session['next'])
            else:
                flash('Logged in successfully!', 'success')
                return redirect(url_for('user.mycards'))

    return render_template('login.html', form=log_in_form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
