DROP DATABASE IF EXISTS ChatApp;
CREATE DATABASE ChatApp;
USE ChatApp;

CREATE TABLE _User (
	UserId INT NOT NULL AUTO_INCREMENT,
	Name VARCHAR(32) NOT NULL,
	Email VARCHAR(64) NOT NULL,
	PhoneNumber INT,
	Password CHAR(128) NOT NULL,
	CONSTRAINT User_PK PRIMARY KEY (UserId)
);

CREATE TABLE Role (
	RoleName VARCHAR(32) NOT NULL,
	AccessLevel INT NOT NULL, -- Integer or char?
	CONSTRAINT Role_PK PRIMARY KEY (RoleName)
);

CREATE TABLE UserRole (
	UserId INT NOT NULL,
	RoleName VARCHAR(32) NOT NULL,
	CONSTRAINT UserRole_FK FOREIGN KEY (UserId) REFERENCES _User(UserId),
	CONSTRAINT UserRoke_PK FOREIGN KEY (RoleName) REFERENCES Role(RoleName)
);

CREATE TABLE ChatSession (
	ChatSessionId INT NOT NULL AUTO_INCREMENT,
	TOPIC VARCHAR(64),
	CONSTRAINT ChatSession_PK PRIMARY KEY (ChatSessionId)
);

CREATE TABLE ChatTopic (
	Topic VARCHAR(64),
	CONSTRAINT ChatTopic_PK PRIMARY KEY (Topic)
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