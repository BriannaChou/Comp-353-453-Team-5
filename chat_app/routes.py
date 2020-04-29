from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import json

from app import app, db, bcrypt, login_manager
from models import User, Customer, Department, ServiceRep, ChatTopic, ChatSession, Message, ChatRequest
from forms import LoginForm, CustomerRegistrationForm, StaffRegistrationForm, PasswordChangeForm, CustomerProfileForm, \
	StaffProfileForm, CustomerBeginChatForm, ChatForm, RequestForm


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
			flash('A service representative will assist you shortly...', 'success')
			return redirect(url_for('home'))
		else:
			requests = ChatRequest.query.filter_by(CustomerId=user.id, Accepted=False).all()
			id_list = ', '.join(map(str, [req.id for req in requests]))
			print(id_list)
			req_url = url_for('chat_request', _method='GET', ids=id_list)
			print(req_url)
			open_chats = ChatSession.query.filter_by(CustomerId=user.id).all()
			return render_template('home-customer.html', title="Begin Chat",
				form=form, user=current_user, requests=requests, req_url=req_url, open_chats=open_chats)
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

@app.route("/request", methods=['GET', 'POST'])
@login_required
def chat_request():
	if current_user.Customer:
		# The js will send a get request with a list of request ids - here, we redirect to any requests that have been accepted
		if request.method == 'GET':
			ids = request.args.get('ids').split(', ')
			print("__________________REQUEST IDS_______________________")
			print(ids)

			for id in ids:
				req = ChatRequest.query.get(id);
				if req and req.Accepted == True:
					print("REQUEST")
					print(req.id)
					print(req.Accepted)
					# The request has been accepted, now get the chat session and redirect
					chat_session = req.ChatSession
					if chat_session:
						return json.dumps({'url': url_for('chat', id=chat_session.id)}), 200, {'ContentType':'application/json'}
					else:
						return json.dumps({'url': url_for('home')}), 200, {'ContentType':'application/json'}
			# If none of the requests have been accepted, just return a 200 status because nothing has been changed
			return json.dumps({'success':True}), 204, {'ContentType':'application/json'}
		else:
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
