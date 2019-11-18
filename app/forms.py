from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


# sign up form
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=80)])
    password_repeat = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=80), EqualTo('password')])
    submit = SubmitField('Sign Up')


# log in form
class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=80)])
    submit = SubmitField('Log In')
