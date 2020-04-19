from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=1, max=32)])
	
	phone = StringField('Phone', validators=[DataRequired(), Length(min=1, max=16)])
	
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=320)])
	
	password = PasswordField('Password', validators=[DataRequired()])
	
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=1, max=60)])
	
	submit = SubmitField('Sign Up')
	
	def validate_email(self, email):
		user = User.query.filter_by(Email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=320)])
	
	password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=60)])
	
	submit = SubmitField('Login')
