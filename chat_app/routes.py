from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db, bcrypt, login_manager
from models import User, Customer, Department, ServiceRep, ChatTopic, ChatSession, Message
from forms import LoginForm, CustomerRegistrationForm, StaffRegistrationForm, PasswordChangeForm, CustomerProfileForm, \
    StaffProfileForm, CustomerBeginChatForm, ChatForm, RepEnterChatForm


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
            chat_session = ChatSession(CustomerId=user.id, Topic=form.chat_topic.data)
            db.session.add(chat_session)
            db.session.commit()
            return redirect(url_for('chat', id=chat_session.ChatSessionId))
        return render_template('home-customer.html', title="Begin Chat", form=form, user=current_user)
    elif user.ServiceRep:
        openSessions = ChatSession.query.all()
        #form = RepEnterChatForm()
        
        #if form.validate_on_submit():
            #return redirect(url_for('chat', id=chat_session.ChatSessionId))
        return render_template('home-staff.html', title="Choose Chat Session", user=current_user, allSessions=openSessions)


@app.route("/chat/<id>", methods=['GET', 'POST'])
@login_required
def chat(id):
    user_id = int(current_user.get_id())
    user = User.query.get(user_id)
    chat_session = ChatSession.query.get(id)
    messages = Message.query.filter_by(ChatSessionId=chat_session.ChatSessionId).order_by(Message.Timestamp)
    form = ChatForm()
    if user.Customer:
        if not chat_session or chat_session.CustomerId != user_id:
            abort(404)
        if request.method == 'POST':
            message = Message(ChatSessionId=chat_session.ChatSessionId, UserId=user_id, Message=form.message.data)
            db.session.add(message)
            db.session.commit()
            return render_template('_messages.html', messages=messages)
        return render_template('chat-customer.html', title="Chat", form=form, messages=messages, user=current_user)
    elif user.ServiceRep:
        # TODO: Add chat functionality for service reps
        if not chat_session or chat_session.ServiceRepId != user_id:
            abort(404)
        pass
