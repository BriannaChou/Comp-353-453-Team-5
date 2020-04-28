from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=320)])
	
	password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=60)])
	
	submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=1, max=60)])


class PasswordChangeForm(PasswordForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')


class CustomerProfileForm(FlaskForm):
    id = IntegerField()
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=32)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=1, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=320)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user and str(user.id) != self.id.data:
            raise ValidationError('That email is taken. Please choose a different one.')


class StaffProfileForm(CustomerProfileForm):
    department = SelectField("Department", validators=[DataRequired()])


class CustomerRegistrationForm(CustomerProfileForm, PasswordForm):
    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class StaffRegistrationForm(CustomerRegistrationForm):
    department = SelectField("Department", validators=[DataRequired()])


class CustomerBeginChatForm(FlaskForm):
    chat_topic = SelectField("Select a chat topic", validators=[DataRequired()])
    submit = SubmitField('Begin Chat')


class ChatForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
