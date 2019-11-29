from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
from app.models import Card
from wtforms import widgets


# figure out all the options we can have for selecting card rarity. This select relies on some things
def get_rarity_options():
    all_cards = Card.query.all()
    all_rarities = list(set([i.rarity for i in all_cards]))
    rarity_options = [(i, i) for i in all_rarities if i]
    return sorted(rarity_options)


RARITY_OPTIONS = [('Common', 'Common'), ('LEGEND', 'LEGEND'), ('Rare', 'Rare'),
                  ('Rare ACE', 'Rare ACE'), ('Rare BREAK', 'Rare BREAK'),
                  ('Rare Holo', 'Rare Holo'), ('Rare Holo EX', 'Rare Holo EX'),
                  ('Rare Holo GX', 'Rare Holo GX'),
                  ('Rare Holo Lv.X', 'Rare Holo Lv.X'),
                  ('Rare Prime', 'Rare Prime'), ('Rare Promo', 'Rare Promo'),
                  ('Rare Rainbow', 'Rare Rainbow'),
                  ('Rare Secret', 'Rare Secret'), ('Rare Ultra', 'Rare Ultra'),
                  ('Shining', 'Shining'), ('Uncommon', 'Uncommon')]


# special field for selecting multiple things
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# sign up form
class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    password_repeat = PasswordField('Password',
                                    validators=[
                                        DataRequired(),
                                        Length(min=6, max=80),
                                        EqualTo('password')
                                    ])
    submit = SubmitField('Sign Up')


# log in form
class LogInForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    rarities = MultiCheckboxField('Rarities:', choices=RARITY_OPTIONS)
    search = StringField('Query:', validators=[Length(min=0, max=80)])
    submit = SubmitField('Search')
