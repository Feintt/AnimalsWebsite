from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class SignupForm(FlaskForm):
    """Login form"""
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password:',
                                     validators=[InputRequired(), EqualTo('password')])
    sign_up = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class EditPetForm(FlaskForm):
    """Edit form"""
    name = StringField('Name', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    bio = StringField('Bio', validators=[InputRequired()])
    submit = SubmitField('Submit')
    delete_pet = SubmitField('Delete Pet')
