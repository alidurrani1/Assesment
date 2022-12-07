from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=5,max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5,max=10)])
   
    password = PasswordField('Password', validators=[DataRequired()])
    c_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

        