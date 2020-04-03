from datetime import datetime
from app import db

class User(db.Model):
	__tablename__ = '_User'
	UserId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	Name = db.Column(db.String(32))
	Email = db.Column(db.String(64))
	PhoneNumber = db.Column(db.String(16))
	Password = db.Column(db.String(128))

class Customer(db.Model):
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'), primary_key=True)

class Department(db.Model):
	DepartmentName = db.Column(db.String(32), primary_key=True)

class ServiceRep(db.Model):
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'), primary_key=True)
	Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))

class ChatTopic(db.Model):
	Topic = db.Column(db.String(64), primary_key=True)
	Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))

class ChatSession(db.Model):
	ChatSessionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	CustomerId = db.Column(db.Integer, db.ForeignKey('Customer.UserId'))
	ServiceRepId = db.Column(db.Integer, db.ForeignKey('ServiceRep.UserId'))
	Topic = db.Column(db.String(64), db.ForeignKey('ChatTopic.Topic'))

class Message(db.Model):
	MessageId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	ChatSessionId = db.Column(db.Integer, db.ForeignKey('ChatSession.ChatSessionId'))
	UserId = db.Column(db.Integer, db.ForeignKey('_User.UserId'))
	Timestamp = db.Column(db.BigInteger)
	Message = db.Column(db.String(512))

