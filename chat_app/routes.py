from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import json

from app import app, db, bcrypt, login_manager
from models import User, Customer, Department, ServiceRep, ChatTopic, ChatSession, Message, ChatRequest
from forms import LoginForm, CustomerRegistrationForm, StaffRegistrationForm, PasswordChangeForm, CustomerProfileForm, \
	StaffProfileForm, CustomerBeginChatForm, ChatForm, RequestForm

from datetime import date

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.errorhandler(401)
def unauthorized(error):
	return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html", title="404"), 404


@app.route("/register-customer", methods=['GET', 'POST'])
def register_customer():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = CustomerRegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(Name=form.name.data, PhoneNumber=form.phone.data, Email=form.email.data, Password=hashed_password, Customer=Customer())
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('login'))
	return render_template('register-customer.html', title='Register', form=form)


@app.route("/register-staff", methods=['GET', 'POST'])
def register_staff():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = StaffRegistrationForm()
	form.department.choices = [("", "")] + [(row.DepartmentName, row.DepartmentName) for row in
											Department.query.order_by(Department.DepartmentName).all()]

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(Name=form.name.data, PhoneNumber=form.phone.data, Email=form.email.data, Password=hashed_password, ServiceRep=ServiceRep(Department=form.department.data))
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('login'))

	return render_template('register-staff.html', title='Register', form=form)


@app.route("/profile", methods=['GET', 'POST'])
def customer_profile():
	form = CustomerProfileForm()
	user_id = current_user.get_id()
	user = User.query.get(user_id)
	form.id.data = user_id

	if form.validate_on_submit():
		user.Name = form.name.data
		user.Email = form.email.data
		user.PhoneNumber = form.phone.data
		db.session.add(user)
		db.session.commit()
		flash('Your profile has been updated.', 'success')
	elif request.method == 'GET':
		if user.ServiceRep:
			return redirect(url_for('staff_profile'))
		form.name.data = user.Name
		form.email.data = user.Email
		form.phone.data = user.PhoneNumber

	return render_template('profile-customer.html', title='Profile', form=form)


@app.route("/staff-profile", methods=['GET', 'POST'])
def staff_profile():
	form = StaffProfileForm()
	user_id = current_user.get_id()
	user = User.query.get(user_id)
	form.id.data = user_id
	form.department.choices = [("", "")] + [(row.DepartmentName, row.DepartmentName) for row in
											Department.query.order_by(Department.DepartmentName).all()]

	if form.validate_on_submit():
		user.Name = form.name.data
		user.Email = form.email.data
		user.PhoneNumber = form.phone.data
		user.ServiceRep.Department = form.department.data
		db.session.add(user)
		db.session.commit()
		flash('Your profile has been updated.', 'success')
	elif request.method == 'GET':
		if user.Customer:
			return redirect(url_for('customer_profile'))
		form.name.data = user.Name
		form.email.data = user.Email
		form.phone.data = user.PhoneNumber
		form.department.choices = [("", "")] + [(row.DepartmentName, row.DepartmentName) for row in
												Department.query.order_by(Department.DepartmentName).all()]
		form.department.data = user.ServiceRep.Department

	return render_template('profile-staff.html', title='Profile', form=form)


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
			flash('Login Unsuccessful. Please check email and password.', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')


@app.route("/password-change", methods=['GET', 'POST'])
@login_required
def password_change():
	form = PasswordChangeForm()

	if form.validate_on_submit():
		user_id = current_user.get_id()
		user = User.query.get(user_id)
		if user and not bcrypt.check_password_hash(user.Password, form.old_password.data):
			flash('Old password is incorrect.', 'danger')
		else:
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user.Password = hashed_password
			db.session.add(user)
			db.session.commit()
			flash('Your password has been changed.', 'success')

	return render_template('password-change.html', title='Change Password', form=form)


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
	user_id = current_user.get_id()
	user = User.query.get(user_id)
	if user.Customer:
		form = CustomerBeginChatForm()
		form.chat_topic.choices = [("", "")] + [(row.Topic, row.Topic) for row in
												ChatTopic.query.order_by(ChatTopic.Topic).all()]
		if form.validate_on_submit():
			# Find the service rep under the specified topic with the least number of open chat sessions
			dept = ChatTopic.query.filter_by(Topic=form.chat_topic.data).first().Department
			request = ChatRequest(CustomerId=user.id, Topic=form.chat_topic.data, Accepted=False)
			db.session.add(request)
			db.session.commit()
			request = ChatRequest.query.filter_by(CustomerId=user.id, Topic=form.chat_topic.data, Accepted=False).first()
			return redirect(url_for('waiting_room', id=request.id))
		else:
			requests = ChatRequest.query.filter_by(CustomerId=user.id, Accepted=False).all()
			open_chats = ChatSession.query.filter_by(CustomerId=user.id).all()
			return render_template('home-customer.html', title="Begin Chat",
				form=form, user=current_user, requests=requests, open_chats=open_chats)
	elif user.ServiceRep:
		chats = ChatSession.query.filter_by(ServiceRepId=user.id).all()

		# Query the request tableand get all the topics that fall under the current user's department
		# then get all requests that match those topics
		reqs = ChatRequest.query \
			.filter_by(Accepted=False) \
			.join(User, User.id == ChatRequest.CustomerId) \
			.add_columns(User.Name) \
			.join(ChatTopic) \
			.filter(ChatTopic.Department == user.ServiceRep.Department) \
			.all() 

		form = RequestForm()
		requests = [(req.ChatRequest.id, '{} has a question regarding {}'.format(req.Name, req.ChatRequest.Topic)) for req in reqs]
		if requests:
			form.set_choices(requests)
		else:
			form = False
		return render_template('home-staff.html', title="Begin Chat", 
				user=current_user, chats=chats, form=form)
	else:
		abort(401)

@app.route("/waiting_room/<id>", methods=['GET'])
@login_required
def waiting_room(id):
	if current_user.Customer:
		req = ChatRequest.query.get(id)
		# The js will send a get request with an id - here, we redirect if the request has been accepted
		if req:
			on_page = request.args.get('present')
			if req.Accepted:
				# The request has been accepted, now get the chat session and redirect
				chat_session = req.ChatSession
				if chat_session:
					return redirect(url_for('chat', id=chat_session.id))
				else:
					flash('Something went wrong - your request has been accepted but we cannot find a corresponding chat session', 'danger')
					# First return a redirect back to this page to try once more - if it fails again, just redirect back home
					if on_page == 'exit':
						return redirect(url_for('home'))
					else:
						return redirect(url_for('waiting_room', id=id, on_page='exit'))
			else:
				if on_page:
					return render_template('waiting.html', user=current_user, req=req), 304
				else:
					return render_template('waiting.html', user=current_user, req=req)
		else:
			return redirect(url_for('home'))
	elif current_user.ServiceRep:
		flash('Only customers have access to this resource', 'danger')
		return redirect(url_for('home'))

@app.route("/request", methods=['POST'])
@login_required
def chat_request():
	if current_user.Customer:
		flash('You do not have access to post to this resource', 'danger')
		abort(401)
	elif current_user.ServiceRep:
		form = RequestForm()
		if form.validate_on_submit:
			req = ChatRequest.query.get(form.requests.data)
			if req.Accepted:
				flash('This request has already been accepted', 'danger')
				return redirect(url_for('home'))
			else:
				req.Accepted = True
				chat_session = ChatSession(CustomerId=req.CustomerId, ServiceRepId=current_user.id, Topic=req.Topic)
				db.session.add(chat_session)
				db.session.commit()
				chat_session = ChatSession.query.filter_by(CustomerId=req.CustomerId, ServiceRepId=current_user.id, Topic=req.Topic).first()
				req.ChatSessionId = chat_session.id
				db.session.commit()
				return redirect(url_for('chat', id=chat_session.id))
		else:
			abort(401)


@app.route("/chat/<id>", methods=['GET', 'POST'])
@login_required
def chat(id):
	user_id = int(current_user.get_id())
	user = User.query.get(user_id)
	chat_session = ChatSession.query.get(id)
	messages = Message.query.filter_by(ChatSessionId=chat_session.id).order_by(Message.Timestamp)
	form = ChatForm()
	form.set_session_id(id)
	if user.Customer:
		if not chat_session or chat_session.CustomerId != user_id:
			abort(404)
		if request.method == 'POST':
			message = Message(ChatSessionId=chat_session.id, UserId=user_id, Message=form.message.data)
			db.session.add(message)
			db.session.commit()
			return render_template('_messages.html', messages=messages)
		return render_template('chat-customer.html', title="Chat", form=form, messages=messages, user=current_user)
	elif user.ServiceRep:
		if not chat_session or chat_session.ServiceRepId != user_id:
			abort(404)
		if request.method == 'POST':
			message = Message(ChatSessionId=chat_session.id, UserId=user_id, Message=form.message.data)
			db.session.add(message)
			db.session.commit()
			return render_template('_messages.html', messages=messages)
		return render_template('chat-customer.html', title="Chat", form=form, messages=messages, user=current_user)

@app.route("/messages/<session_id>", methods=['GET'])
@login_required
def messages(session_id):
    messages = Message.query.filter_by(ChatSessionId=session_id).order_by(Message.Timestamp)
    return render_template('_messages.html', messages=messages)


@app.route("/request/<request_id>", methods=['DELETE'])
@login_required
def delete_request(request_id):
	user_id = int(current_user.get_id())
	request = ChatRequest.query.get(request_id)
	if not request or request.Customer.id != user_id:
		abort(404)
	db.session.delete(request)
	db.session.commit()
	return '', 200

@app.route("/report", methods=['GET'])
@login_required
def report():
	user_id = current_user.get_id()
	user = User.query.get(user_id)
	if not user.ServiceRep:
		abort(401)

	# Aggregate function
	sql_count = "SELECT COUNT(*) FROM ChatSession WHERE id = " + user_id
	total = db.engine.execute(sql_count).scalar()
	# TODO: Write additional queries for questions 8, 11, and 13 using .fetchone() and .fetchall() when appropriate

	date_format = date.today();
	current_date = date_format.strftime("%Y-%m-%d %H:%M:%S")

	daily_messages = "SELECT COUNT(MessageId) FROM Message WHERE UserId = " + user_id + " AND Timestamp > "  + "current_date" 
	total_messages = db.engine.execute(daily_messages).scalar()
	
	best_sql= "select * from ServiceRep where id = (select sr.id from ChatSession cs join ServiceRep sr on cs.ServiceRepId = sr.id group by sr.id order by count(cs.id) desc limit 1)"
	best_rep = db.engine.execute(best_sql).scalar()

	dept_sql = "SELECT Department FROM ServiceRep WHERE id =" + user_id
	rep_dept = db.engine.execute(dept_sql).scalar()

	return render_template('staff-report.html', title="Service Rep Report", user=current_user, total=total, total_messages=total_messages, best_rep=best_rep, rep_dept=rep_dept)
