from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	__tablename__ = '_User'
	__table_args__ = {'extend_existing': True}
	id = db.Column('UserId', db.Integer, autoincrement=True, primary_key=True)
	Name = db.Column(db.String(32))
	Email = db.Column(db.String(64))
	PhoneNumber = db.Column(db.String(16))
	Password = db.Column(db.String(128), nullable=False)

	def __repr__(self):
		return '<User {}>'.format(self.Email)

class Customer(db.Model):
	__table_args__ = {'extend_existing': True}
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'), primary_key=True)

class Department(db.Model):
	__table_args__ = {'extend_existing': True}
	DepartmentName = db.Column(db.String(32), primary_key=True)

class ServiceRep(db.Model):
	__table_args__ = {'extend_existing': True}
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'), primary_key=True)
	Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))

class ChatTopic(db.Model):
	__table_args__ = {'extend_existing': True}
	Topic = db.Column(db.String(64), primary_key=True)
	Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))

class ChatSession(db.Model):
	__table_args__ = {'extend_existing': True}
	ChatSessionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	CustomerId = db.Column(db.Integer, db.ForeignKey('Customer.UserId'))
	ServiceRepId = db.Column(db.Integer, db.ForeignKey('ServiceRep.UserId'))
	Topic = db.Column(db.String(64), db.ForeignKey('ChatTopic.Topic'))

class Message(db.Model):
	__table_args__ = {'extend_existing': True}
	MessageId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	ChatSessionId = db.Column(db.Integer, db.ForeignKey('ChatSession.ChatSessionId'))
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'))
	Timestamp = db.Column(db.BigInteger)
	Message = db.Column(db.String(512))

