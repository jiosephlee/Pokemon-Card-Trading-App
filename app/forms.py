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


def get_type_options():
    all_cards = Card.query.all()
    all_types = list(set([i.type for i in all_cards]))
    types_options = [(i, i) for i in all_types if i]
    return sorted(types_options)


RARITY_OPTIONS = [('Common', 'Common'), ('LEGEND', 'LEGEND'), ('Rare', 'Rare'),
                  ('Rare ACE', 'Rare ACE'), ('Rare BREAK', 'Rare BREAK'),
                  ('Rare Holo', 'Rare Holo'), ('Rare Holo EX', 'Rare Holo EX'),
                  ('Rare Holo GX', 'Rare Holo GX'),
                  ('Rare Holo Lv.X', 'Rare Holo Lv.X'),
                  ('Rare Prime', 'Rare Prime'), ('Rare Promo', 'Rare Promo'),
                  ('Rare Rainbow', 'Rare Rainbow'),
                  ('Rare Secret', 'Rare Secret'), ('Rare Ultra', 'Rare Ultra'),
                  ('Shining', 'Shining'), ('Uncommon', 'Uncommon')]

TYPE_OPTIONS = [('Colorless', 'Colorless'),
                ('Colorless,Psychic', 'Colorless,Psychic'),
                ('Darkness', 'Darkness'),
                ('Darkness,Darkness', 'Darkness,Darkness'),
                ('Darkness,Metal', 'Darkness,Metal'),
                ('Darkness,Psychic', 'Darkness,Psychic'), ('Dragon', 'Dragon'),
                ('Fairy', 'Fairy'), ('Fairy,Psychic', 'Fairy,Psychic'),
                ('Fairy,Water', 'Fairy,Water'), ('Fighting', 'Fighting'),
                ('Fighting,Darkness', 'Fighting,Darkness'),
                ('Fighting,Metal', 'Fighting,Metal'), ('Fire', 'Fire'),
                ('Fire,Darkness', 'Fire,Darkness'),
                ('Fire,Grass', 'Fire,Grass'),
                ('Fire,Lightning', 'Fire,Lightning'),
                ('Fire,Metal', 'Fire,Metal'), ('Fire,Water', 'Fire,Water'),
                ('Grass', 'Grass'), ('Grass,Darkness', 'Grass,Darkness'),
                ('Grass,Metal', 'Grass,Metal'), ('Lightning', 'Lightning'),
                ('Lightning,Darkness', 'Lightning,Darkness'),
                ('Lightning,Grass', 'Lightning,Grass'),
                ('Lightning,Metal', 'Lightning,Metal'),
                ('Lightning,Water', 'Lightning,Water'), ('Metal', 'Metal'),
                ('Metal,Darkness', 'Metal,Darkness'),
                ('Metal,Fighting', 'Metal,Fighting'), ('Psychic', 'Psychic'),
                ('Psychic,Darkness', 'Psychic,Darkness'),
                ('Psychic,Metal', 'Psychic,Metal'), ('Water', 'Water'),
                ('Water,Darkness', 'Water,Darkness'),
                ('Water,Fighting', 'Water,Fighting'),
                ('Water,Fire', 'Water,Fire'), ('Water,Metal', 'Water,Metal')]


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
    rarities = MultiCheckboxField('Filter by rarity:', choices=RARITY_OPTIONS)
    types = MultiCheckboxField('Filter by type:', choices=TYPE_OPTIONS)
    search = StringField('Query:', validators=[Length(min=0, max=80)])
    submit = SubmitField('Search')
