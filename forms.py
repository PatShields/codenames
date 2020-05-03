from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange


class GenerateCurrentForm(FlaskForm):
    board_number = IntegerField('Board Number', validators=[DataRequired()])
    submit_num = SubmitField('View Existing Boards')
    adult_check = BooleanField('Dirty Words')


class GenerateNewForm(FlaskForm):
    submit_new = SubmitField('Start New Game')
    adult_check = BooleanField('Dirty Words')


class UndoCoverForm(FlaskForm):
    submit_undo = SubmitField('Undo Last Card')


class MakeDirtyForm(FlaskForm):
    submit_dirty = SubmitField('Get Dirty!')


class MakeCleanForm(FlaskForm):
    submit_clean = SubmitField('Clean It Up!')


class SubmitWordsForm(FlaskForm):
    word = TextAreaField('Words ', validators=[DataRequired()])
    adult = BooleanField('Dirty Words')
    password = PasswordField('Password', [DataRequired(), EqualTo(
        'confirm', message='Passwords must match')])
    submit = SubmitField('Submit')


class CoverCardsForm(FlaskForm):
    space_choices = [('1', '1'), ('2', '2'), ('3', '3'),
                     ('4', '4'), ('5', '5')]
    color_choices = [('neutral', 'neutral'), ('blue', 'blue'),
                     ('red', 'red'), ('assassin', 'assassin')]
    row = SelectField('Row', choices=space_choices)
    col = SelectField('Column', choices=space_choices)
    color = SelectField('Type', choices=color_choices)
    submit_cover = SubmitField('Cover Card')
