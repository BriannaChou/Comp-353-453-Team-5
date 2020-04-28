DROP DATABASE IF EXISTS ChatApp;
CREATE DATABASE ChatApp;
USE ChatApp;

CREATE TABLE User (
	id INT NOT NULL AUTO_INCREMENT,
	Name VARCHAR(32) NOT NULL,
	Email VARCHAR(64) NOT NULL,
	PhoneNumber VARCHAR(16),
	Password CHAR(128) NOT NULL,
	CONSTRAINT User_PK PRIMARY KEY (id)
);

CREATE TABLE Customer (
	id INT NOT NULL,
	CONSTRAINT Customer_FK FOREIGN KEY (id) REFERENCES User(id)
);

CREATE TABLE Department (
	DepartmentName VARCHAR(32) NOT NULL,
	CONSTRAINT Department_PK PRIMARY KEY (DepartmentName)
);

CREATE TABLE ServiceRep (
	id INT NOT NULL,
	Department VARCHAR(32) NOT NULL,
	CONSTRAINT ServiceRep_FK1 FOREIGN KEY (id) REFERENCES User(id),
	CONSTRAINT ServiceRep_FK2 FOREIGN KEY (Department) REFERENCES Department(DepartmentName)
);

CREATE TABLE ChatTopic (
	Topic VARCHAR(64) NOT NULL,
	Department VARCHAR(32) NOT NULL,
	CONSTRAINT Topic_PK PRIMARY KEY (Topic),
	CONSTRAINT Topic_FK FOREIGN KEY (Department) REFERENCES Department(DepartmentName)
);

CREATE TABLE ChatSession (
	id INT NOT NULL AUTO_INCREMENT,
	CustomerId INT NOT NULL,
	ServiceRepId INT NOT NULL,
	Topic VARCHAR(64),
	CONSTRAINT ChatSession_PK PRIMARY KEY (id),
	CONSTRAINT ChatSession_FK1 FOREIGN KEY (CustomerId) REFERENCES Customer(id),
	CONSTRAINT ChatSession_FK2 FOREIGN KEY (ServiceRepId) REFERENCES ServiceRep(id),
	CONSTRAINT ChatSession_FK3 FOREIGN KEY (Topic) REFERENCES ChatTopic(Topic)
);

CREATE TABLE Message (
	MessageId INT NOT NULL AUTO_INCREMENT,
	ChatSessionId INT NOT NULL,
	UserId INT NOT NULL,
	Timestamp DateTime NOT NULL,
	Message VARCHAR(512),
	CONSTRAINT Message_PK PRIMARY KEY (MessageId),
	CONSTRAINT Message_FK1 FOREIGN KEY (ChatSessionId) REFERENCES ChatSession(id),
	CONSTRAINT Message_FK2 FOREIGN KEY (UserId) REFERENCES User(id)
);

CREATE TABLE ChatRequest (
	id INT NOT NULL AUTO_INCREMENT,
	CustomerId INT NOT NULL,
	Topic VARCHAR(64) NOT NULL,
	Accepted BOOLEAN DEFAULT false,
	CONSTRAINT Request_PK PRIMARY KEY (id),
	CONSTRAINT Request_FK1 FOREIGN KEY (CustomerId) REFERENCES Customer(id),
	CONSTRAINT Request_FK2 FOREIGN KEY (Topic) REFERENCES ChatTopic(Topic)
);
