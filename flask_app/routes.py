from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from app import app, db, bcrypt, login_manager
from models import User, Customer, Department, ServiceRep, ChatTopic, ChatSession, Message
from forms import RegistrationForm, LoginForm

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=int(user_id)).first()

@app.errorhandler(401)
def unauthorized(error):
	return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html", title="404"), 404

@app.route("/")
@login_required
def home():
	return render_template('home.html', title="Dashboard", user=current_user)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(Name=form.name.data, PhoneNumber=form.phone.data, Email=form.email.data, Password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(Email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.Password, form.password.data):
			print("You're logged in: {}".format(user))
			login_user(user)
			next_page = request.args.get('next')
			print("NEXT page: {}".format(next_page))
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')
