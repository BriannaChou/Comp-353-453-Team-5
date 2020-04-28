# Customer Support Chat App

This repository holds the code for a customer support chat application. This app was created for COMP 353 (Database Programming) by Brianna Chou, Paul Macniak, and Jack Kotheimer. The purpose of the app is to be a simple interface for customers to request the help of a service representative and chat with them in a (relatively) live environment.

# Tools

- HTML/Bootstrap
- Python Flask
- MySQL
- PHPMyAdmin (for administration and testing)
- Bash Scripting (for automation)

### How we used these Tools

This web app utilizes Python Flask to create a REST API which is called upon by a basic HTML/Bootstrap front end with forms. The Flask API uses a library to make queries back and forth with a MySQL database. PHPMyAdmin was used to ensure each query was being properly executed. Bash scripts were written to quicky start and refresh the Flask service and to quickly execute SQL queries to refresh the database if any changes were made to the structure. 

### Why we used these tools

We chose Python Flask for the API because our main learning goal for this project was to learn how to properly structure a database around a business model and appropriately query it. Flask has a shallow learning curve and allows for very simple database queries and dynamic HTML generation. This allowed us to focus most of our attention on the structure and logic of the database.
