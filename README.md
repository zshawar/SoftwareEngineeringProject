# Events App - RSVME

Events App - RSVME is a tool that allows users to create and manage their own events and join events created by other users. 
The application includes the following features:
* User account registration / sign-in
* Displays a list of user's events
* Displays a list of user's joined events
* View/edit an event
* Delete event(s)
* Add/report reviews on an event
* Create new events
* Reporting events
* Joining events
* Adding thumbnail pictures to events
* Sorting events by capacity, time, location, or name
* Admin panel for users that have been assigned the admin role
* Admins can delete or dismiss reported events and reviews
* Extra verification for events before user is allowed to view them
* User can reset their password

## Prerequisites

Before you run the app ensure you have met the following requirements:
* You have installed git version 2.22 or higher (https://git-scm.com/downloads)
* You have installed python version 3.6 or higher (https://www.python.org/downloads/)
* You have installed SQLite (version 3 / SQLite3) (https://www.sqlite.org/download.html)
* You have installed Flask web framework
* You have installed wtforms, Flask-WTF, email_validator, and bcrypt

## Installing Events App - RSVME

To run Events App - RSVME locally, follow these steps:

In terminal type the following commands:

Clone the project from Github
```
git clone https://github.com/zshawar/SoftwareEngineeringProject.git
```
Change into the newly created directory
```
cd SoftwareEngineeringProject
```
cd RSVPme
```
Create a Python virtual environment
```
python3 -m venv venv
```
- MacOS:
```
source venv/bin/activate
```
- Windows:
```
mypthon Scripts activate OR source venv/Scripts/Activate
```
Install Flask framework
```
pip3 install flask
```
Install SQLAlchemy
```
pip3 install flask-sqlalchemy
```
Install modules and bcrypt
```
pip3 install wtforms
pip3 install Flask-WTF
pip3 install email_validator
pip3 install bcrypt
```
Set flask environment variable 

- MacOS:
```
export FLASK_APP=routes.py
```
- Windows:
```
set FLASK_APP=routes.py
```
Start the Flask server
```
flask run
```
Open web browser and go to
```
http://localhost:5000/
```

## Contributors
* @Zaina Shawar
* @JustCallMeJoe1
* @ChristinaSarkisyan
* @Flarp 
* @laboufoul

