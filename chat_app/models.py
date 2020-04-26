from sqlalchemy.orm import relationship

from app import db
from flask_login import UserMixin


class Customer(db.Model):
    __tablename__ = 'Customer'
    __table_args__ = {'extend_existing': True}
    UserId = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)


class Department(db.Model):
    __tablename__ = 'Department'
    __table_args__ = {'extend_existing': True}
    DepartmentName = db.Column(db.String(32), primary_key=True)


class ServiceRep(db.Model):
    __tablename__ = 'ServiceRep'
    __table_args__ = {'extend_existing': True}
    UserId = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String(32))
    Email = db.Column(db.String(64))
    PhoneNumber = db.Column(db.String(16))
    Password = db.Column(db.String(128), nullable=False)
    Customer = relationship(Customer, backref='User', uselist=False)
    ServiceRep = relationship(ServiceRep, backref='User', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.Email)


class ChatTopic(db.Model):
    __tablename__ = 'ChatTopic'
    __table_args__ = {'extend_existing': True}
    Topic = db.Column(db.String(64), primary_key=True)
    Department = db.Column(db.String(32), db.ForeignKey('Department.DepartmentName'))


class ChatSession(db.Model):
    __tablename__ = 'ChatSession'
    __table_args__ = {'extend_existing': True}
    ChatSessionId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customer.UserId'))
    ServiceRepId = db.Column(db.Integer, db.ForeignKey('ServiceRep.UserId'))
    Topic = db.Column(db.String(64), db.ForeignKey('ChatTopic.Topic'))


class Message(db.Model):
    __tablename__ = 'Message'
    __table_args__ = {'extend_existing': True}
    MessageId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ChatSessionId = db.Column(db.Integer, db.ForeignKey('ChatSession.ChatSessionId'))
    UserId = db.Column(db.Integer, db.ForeignKey('User.id'))
    Timestamp = db.Column(db.TIMESTAMP)
    Message = db.Column(db.String(512))
