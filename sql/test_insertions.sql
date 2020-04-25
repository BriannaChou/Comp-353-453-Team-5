USE ChatApp;

INSERT INTO Department VALUES ('Billing');
INSERT INTO Department VALUES ('Shipping');
INSERT INTO Department VALUES ('Tech Support');

INSERT INTO User (Name, Email, PhoneNumber, Password)
	VALUES
	("Jack Kotheimer", "jkotheimer@luc.edu", "773-202-LUNA", "b73872e0e3a0b22dc599a7c4bbf1c8193a2a1b4c3efaba9ea79e9b7f4777f4a0"),
	("Paul Macniack", "pmacniak@luc.edu", "800-588-2300", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),
	("Brianna Chou", "bchou@luc.edu", "773-202-5000", "16cf1ed06f67efd71491b9af4e6517c46ab8640db80357db5ce8cd7fa77f2ecf");
