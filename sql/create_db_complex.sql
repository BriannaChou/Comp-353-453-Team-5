DROP DATABASE IF EXISTS ChatApp;
CREATE DATABASE ChatApp;
USE ChatApp;

CREATE TABLE _User (
	UserId INT NOT NULL AUTO_INCREMENT,
	Name VARCHAR(32) NOT NULL,
	Email VARCHAR(64) NOT NULL,
	PhoneNumber VARCHAR(16),
	Password CHAR(128) NOT NULL,
	CONSTRAINT User_PK PRIMARY KEY (UserId)
);

CREATE TABLE Customer (
	UserId INT NOT NULL,
	CONSTRAINT Customer_FK FOREIGN KEY (UserId) REFERENCES _User(UserId)
);

CREATE TABLE Department (
	DepartmentName VARCHAR(32) NOT NULL,
	CONSTRAINT Department_PK PRIMARY KEY (DepartmentName)
);

CREATE TABLE ServiceRep (
	UserId INT NOT NULL,
	Department VARCHAR(32) NOT NULL,
	CONSTRAINT ServiceRep_FK1 FOREIGN KEY (UserId) REFERENCES _User(UserId),
	CONSTRAINT ServiceRep_FK2 FOREIGN KEY (Department) REFERENCES Department(DepartmentName)
);

CREATE TABLE ChatTopic (
	Topic VARCHAR(64) NOT NULL,
	Department VARCHAR(32) NOT NULL,
	CONSTRAINT Topic_PK PRIMARY KEY (Topic),
	CONSTRAINT Topic_FK FOREIGN KEY (Department) REFERENCES Department(DepartmentName)
);

CREATE TABLE ChatSession (
	ChatSessionId INT NOT NULL AUTO_INCREMENT,
	CustomerId INT NOT NULL,
	ServiceRepId INT NOT NULL,
	Topic VARCHAR(64),
	CONSTRAINT ChatSession_PK PRIMARY KEY (ChatSessionId),
	CONSTRAINT ChatSession_FK1 FOREIGN KEY (CustomerId) REFERENCES Customer(UserId),
	CONSTRAINT ChatSession_FK2 FOREIGN KEY (ServiceRepId) REFERENCES ServiceRep(UserId),
	CONSTRAINT ChatSession_FK3 FOREIGN KEY (Topic) REFERENCES ChatTopic(Topic)
);

CREATE TABLE Message (
	MessageId INT NOT NULL AUTO_INCREMENT,
	ChatSessionId INT NOT NULL,
	UserId INT NOT NULL,
	Timestamp BIGINT,
	Message VARCHAR(512),
	CONSTRAINT Message_PK PRIMARY KEY (MessageId),
	CONSTRAINT Message_FK1 FOREIGN KEY (ChatSessionId) REFERENCES ChatSession(ChatSessionId),
	CONSTRAINT Message_FK2 FOREIGN KEY (UserId) REFERENCES _User(UserId)
);
