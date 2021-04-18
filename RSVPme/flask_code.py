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
    # Check to see if there is a user saved in the current session
    if session.get("user"):
        return render_template("home.html", user=session["user"])

    return render_template("login.html")  # There is no user in the current session, please log in

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

        # Redirect the user after registering to the home page with their session
        return redirect(url_for("home"))

    # Breaks out of if statement, user did something incorrect, just reloads the register page with the form again
    return render_template("register.html", form=form)

#----------------------------add event functionality---------------------------------------#
@app.route('/events/create', methods=['POST', 'GET'])
def create_event():
    form = EventForm()

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

        return redirect(url_for('get_events'))
    else:
        return render_template('create_event.html', form=form)


#-----------------------------my events page-------------------------------------------#
@app.route('/my_events', methods=['GET'])
def get_user_events():

    # Verify that the user is logged into the current session...
    if session.get("user"):

        # Retrieve the permission for the specific logged in user
        subqueryPermission = db.session.query(Permission).filter_by(userID=session["user"], role="Owner").subquery().all()

        # Retrieve all of the events based on the user's permissions
        usersEvents = db.session.query(Event).filter_by(eventID=subqueryPermission.eventID).all()

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

    myEvents = db.session.query(Event).filter_by(eventID=event_id).one()  # Retrieve a specific event from the database

    return render_template('event.html', event=myEvents)


#--------------------------------------get events--------------------------------------#
#                for getting all of the events                                         #
#--------------------------------------------------------------------------------------#

@app.route('/events')
def get_events():

    #**********************add code to re-verify login here*************************#

    myEvents = db.session.query(Event).limit(9).all()  # Get 5 recent events from the database

    return render_template('events.html', events=myEvents)  # Render the events.html page with the events gathered from the database (Array of events)


#--------------------------------------edit event--------------------------------------#
#                for modifying an event                                                #
#--------------------------------------------------------------------------------------#

@app.route('/home/events/edit/<event_id>', methods = ['GET', 'POST'])
def modify_event(event_id):
    if request.method == 'POST':
        #**********************add code to re-verify login here*************************#
        name = request.form['name']	
        dateofEvent = request.form['dateofEvent']
        description = request.form['description']               #gets all of the info from the input boxes
        location = request.form['location']
        capacity = request.form['capacity']
        
        event = db.session.query(Event).filter_by(id=event_id).one()    #gets the event we're working with 

        event.name = name
        event.dateofEvent = dateofEvent
        event.description = description                                 #updates the feilds of the event we're working with with what we got from the input boxes
        event.name = location
        event.capacity = capacity

        db.session.add(event)                                            #puts the updated version of the event back into the database
        db.session.commit()

        return redirect(url_for('get_user_events'))
    else:
        event = db.session.query(Event).filter_by(id=event_id).one()

        return render_template('modify_event.html', event_id=event_id)

#------------------------------------delete event--------------------------------------#
#                 for removing an event                                                #
#--------------------------------------------------------------------------------------#

@app.route('/events/delete/<event_id>', methods=['POST'])	
def delete_event(event_id):
    event = db.session.query(Event).filter_by(id=event_id).one()
    #**********************add code to re-verify login here*************************#
    db.session.delete(event) 
    db.session.commit()

    return redirect(url_for('get_events'))




#--------------------------run statement------------------------------------#
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True) 	#this is directly from class so see if we need to change anything?
