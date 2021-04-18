#--------------------------import statements----------------------------------#
import os
import bcrypt  # Hashing and Salting passwords library stuff
from flask import Flask   
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from database import db
from forms import LoginForm, RegisterForm, EventForm
from models import User, Event, Role, Permission
from datetime import datetime



#--------------------------setup----------------------------------------------#
app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rsvpme.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables a functionality to alert of a DB Change
app.config["SECRET_KEY"] = "BruhMoment3155"  # Secret Key for session ( I dont know what this should be, does it matter? )
db.init_app(app)

with app.app_context():
    db.create_all()   # run under the app context

#----------------------------home page---------------------------------------#
@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    form = LoginForm()  # Initialize the form object to be the login form
    # Check to see if there is a user saved in the current session
    if session.get("user"):
        return render_template("home.html", user=session["user"])

    return render_template("login.html", form=form)  # There is no user in the current session, please log in

#----------------------------login functionality---------------------------------------#
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()  # Initialize the form object to be the login form

    # Validate the user submitted information (POST METHOD)
    if form.validate_on_submit():

        # The user exists, grab that single user (use the .one() method to grab from database)
        inputtedEmail = request.form["email"]   # Grab the email submitted
        inputtedPassword = request.form["password"].encode("utf-8")  # Grab the password submitted, encode it
        theUser = db.session.query(User).filter_by(email=inputtedEmail).one()

        # Check the password to see if it matches the hash stored in the database
        if bcrypt.checkpw(inputtedPassword, theUser.password):

            # The inputted password matches the stored hash in the database, log the user into the session
            session["user"] = theUser.username
            session["userID"] = theUser.userID
            session["email"] = theUser.email

            # Render the home page for the logged in user
            return redirect(url_for("home"))

        # The password check has failed, the person logging in inputting the incorrect information
        form.password.errors = ["Incorrect username or password entered"]
        return render_template("login.html", form=form)
    else:
        # Since it is not a post request, it must be a get request to first log in, just render the template for logging in
        return render_template("login.html", form=form)

#----------------------------logout functionality---------------------------------------#
@app.route('/logout')
def logout():
    # Check to see if there is a user saved in the session
    if session.get("user"):
        session.clear()

    return redirect(url_for("login"))

#----------------------------register functionality---------------------------------------#
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()  # Initialize the form object to be the register form

    if request.method == "POST" and form.validate_on_submit():
        # Salt and Hash the password entered.
        hashedPassword = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())

        # Retrieve all of the entered information from the form
        userName = request.form["username"]
        email = request.form["email"]

        # Create a new user and put them in the database
        newUser = User(userName, email, hashedPassword)

        # Add this new user object to the database
        db.session.add(newUser)
        db.session.commit()

        # Save the user to the current session
        session["user"] = userName  # User in the session is the username
        session["userID"] = newUser.userID  # User ID from the database table is the userID
        session["email"] = email

        # Redirect the user after registering to the home page with their session
        return redirect(url_for("home"))

    # Breaks out of if statement, user did something incorrect, just reloads the register page with the form again
    return render_template("register.html", form=form)

#----------------------------add event functionality---------------------------------------#
@app.route('/events/create', methods=['POST', 'GET'])
def create_event():
    form = EventForm()

    # Verify the user is currently signed in, check the session
    if session.get("user"):
        if request.method == 'POST' and form.validate_on_submit():
            name = request.form['eventName']
            dateStart = request.form['dateStart']
            dateEnd = request.form['dateEnd']
            description = request.form['description']
            # image = request.form['image']
            location = request.form['location']
            capacity = request.form['capacity']

            newEvent = Event(name, capacity, description, location, dateStart, dateEnd, "")
            db.session.add(newEvent)
            db.session.commit()

            # Add permission entry to the row after creating the event
            role = "Owner"
            eventID = newEvent.eventID
            sessionID = session["userID"]

            newPermission = Permission(eventID, sessionID, role)
            db.session.add(newPermission)
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            return render_template('create_event.html', form=form, user=session['user'])
    else:
        return redirect(url_for("login"))


#-----------------------------my events page-------------------------------------------#
@app.route('/my_events', methods=['GET'])
def get_user_events():

    # Verify that the user is logged into the current session...
    if session.get("user"):

        # Retrieve the eventID from the permission table by filtering to a specific user who is logged in and is an owner of the event.
        subqueryPermission = db.session.query(Permission.eventID).filter_by(userID=session["userID"], role="Owner").subquery()

        # Retrieve all of the events based on the subquery (The eventID from the permission table by filtering with logged in user and owner role)
        usersEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryPermission)).all()

        # Return the myEvents template and pass the events grabbed from the database as well as the user stored in the current session
        return render_template("my_events.html", events=usersEvents, user=session["userID"])

    # The user is not logged in, they need to log in first to view their events. Redirect them to login.
    else:
        return redirect(url_for("login"))


#--------------------------------------get event---------------------------------------#
#                for very specifically showing one event in particular                 #
#--------------------------------------------------------------------------------------#

@app.route('/events/<event_id>')
def get_event(event_id):
    #**********************add code to re-verify login here*************************#
    # login verification; if user is logged in and saved in session
    if session.get("user"):

        myEvents = db.session.query(Event).filter_by(eventID=event_id).one()  # Retrieve a specific event from the database

        return render_template('event.html', event=myEvents, user=session['user'])
    # if user is not logged in they must be redirected to login page
    else:
        return redirect(url_for("login"))


#--------------------------------------get events--------------------------------------#
#                for getting all of the events                                         #
#--------------------------------------------------------------------------------------#

@app.route('/events')
def get_events():
    #**********************add code to re-verify login here*************************#
    # login verification; if user is logged in and saved in session  
    if session.get("user"):

        myEvents = db.session.query(Event).limit(9).all()  # Get 5 recent events from the database

        return render_template('events.html', events=myEvents, user=session['user'])  # Render the events.html page with the events gathered from the database (Array of events)
    # if user is not logged in they must be redirected to login page
    else:
        return redirect(url_for("login"))

#--------------------------------------edit event--------------------------------------#
#                for modifying an event                                                #
#--------------------------------------------------------------------------------------#

@app.route('/events/edit/<event_id>', methods = ['GET', 'POST'])
def modify_event(event_id):
    form = EventForm()
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get data
            name = request.form['eventName']
            dateStart = request.form['dateStart']
            dateEnd = request.form['dateEnd']
            description = request.form['description']
            # image = request.form['image']
            location = request.form['location']
            capacity = request.form['capacity']
            event = db.session.query(Event).filter_by(eventID=event_id).one()

            # update data
            event.name = name
            event.dateStart = datetime.strptime(dateStart, '%Y-%m-%dT%H:%M')
            event.dateEnd = datetime.strptime(dateEnd, '%Y-%m-%dT%H:%M')
            event.description = description
            event.location = location
            event.capacity = capacity

            # updates event in db
            # db.session.add(event)
            db.session.commit()

            return redirect(url_for('get_events'))

        else:
            # GET request - show new event form to edit event
            # retrieve event from database
            my_event = db.session.query(Event).filter_by(eventID=event_id).one()
            form.eventName.data = my_event.name
            form.dateStart.data = my_event.dateStart
            form.dateEnd.data = my_event.dateEnd
            form.description.data = my_event.description
            form.location.data = my_event.location
            form.capacity.data = my_event.capacity
            # form.image.data = my_event.relativePath

            return render_template('create_event.html', form=form, event=my_event, user=session['user'])
    else:
        # user is not in session - redirect to login
        return redirect(url_for('login'))

#------------------------------------delete event--------------------------------------#
#                 for removing an event                                                #
#--------------------------------------------------------------------------------------#

@app.route('/events/delete/<event_id>', methods=['POST'])	
def delete_event(event_id):

    # login verification; if user is logged in and saved in session  
    if session.get("user"):

        event = db.session.query(Event).filter_by(eventID=event_id).one()
        db.session.delete(event) 
        db.session.commit()

        return redirect(url_for('get_events'))
    
    else:
        # if user is not in session they must be redirected to login page
        return redirect(url_for('login'))


#---------------------get user profile--------------------------------------------------#
#               view the user's profile                                                 #
#---------------------------------------------------------------------------------------#
@app.route("/my_profile")
def get_user_profile():
    if session.get("user"):
        return render_template("user_profile.html", user=session["user"], email=session["email"])
    else:
        redirect(url_for("login"))

#--------------------------run statement------------------------------------#
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True) 	#this is directly from class so see if we need to change anything?
