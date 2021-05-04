#--------------------------import statements----------------------------------#
import os
import bcrypt  # Hashing and Salting passwords library stuff
from werkzeug.utils import secure_filename # apparently included in flask
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from database import db
from forms import LoginForm, RegisterForm, EventForm, ReviewForm, PassChangeForm
from models import User, Event, Role, Permission, Report
from datetime import datetime
from models import Review as Review


#--------------------------setup----------------------------------------------#
app = Flask(__name__)     # create an app
app.jinja_env.globals.update(zip=zip)  # Long story, but allows jinja to iterate between 2 parallel items ( It's for reviews )
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
        return render_template("home.html", user=session["user"], admin=session["admin"])

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
            session["admin"] = theUser.admin
            session["verifyCount"] = 0

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
        totalEventsCreated = 0
        totalEventsJoined = 0
        totalEventReviews = 0

        # Create a new user and put them in the database
        newUser = User(userName, email, hashedPassword, totalEventsCreated, totalEventsJoined, totalEventReviews)

        # Add this new user object to the database
        db.session.add(newUser)
        db.session.commit()

        # Save the user to the current session
        session["user"] = userName  # User in the session is the username
        session["userID"] = newUser.userID  # User ID from the database table is the userID
        session["email"] = email
        session["verifyCount"] = 0
        session["admin"] = False

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
            # Grab all of the information provided from the user in the forms
            name = request.form['eventName']
            dateStart = request.form['dateStart']
            dateEnd = request.form['dateEnd']
            description = request.form['description']
            image = request.files['image']
            location = request.form['location']
            capacity = request.form['capacity']
            privacySetting = request.form.get('privacySetting', False)

            # Saves the image to the local directory, the path goes to the server
            filename = datetime.now().strftime("%Y%M%d%H%S") + secure_filename(image.filename)
            image.save(os.path.join("./static/img", filename))

            # Create a new event in the database with the information provided from the user
            newEvent = Event(name, capacity, description, location, dateStart, dateEnd, filename, privacySetting, session['userID'])
            db.session.add(newEvent)
            db.session.commit()

            # Add permission entry to the row after creating the event
            role = "Owner"
            eventID = newEvent.eventID
            sessionID = session["userID"]

            newPermission = Permission(eventID, sessionID, role)
            db.session.add(newPermission)
            db.session.commit()

            # Grab the user's account and add 1 to the running sum of events created by that user
            theUser = db.session.query(User).filter_by(userID=sessionID).one()
            theUser.totalEventsCreated += 1
            db.session.commit()

            return redirect(url_for('get_events'))
        else:
            return render_template('create_event.html', form=form, user=session['user'], admin=session["admin"])
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

        # Retrieve all of the events that the user has joined. Create a subquery that looks for eventIDs with the user as an attendee
        subqueryPermission2 = db.session.query(Permission.eventID).filter_by(userID=session["userID"], role="Attendee").subquery()

        # Retrieve all of the events based on the subqueryPermission2 query
        userJoinedEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryPermission2)).all()

        # Return the myEvents template and pass the events grabbed from the database as well as the user stored in the current session
        return render_template("my_events.html", events=usersEvents, jEvents=userJoinedEvents, user=session["userID"], admin=session["admin"])

    # The user is not logged in, they need to log in first to view their events. Redirect them to login.
    else:
        return redirect(url_for("login"))


#--------------------------------------get event---------------------------------------#
#                for very specifically showing one event in particular                 #
#--------------------------------------------------------------------------------------#
@app.route('/events/<event_id>')
def get_event(event_id):
    # login verification; if user is logged in and saved in session
    if session.get("user"):
        prev_res = db.session.query(Permission).filter_by(eventID=event_id, userID=session["userID"]).count()
        myEvents = db.session.query(Event).filter_by(eventID=event_id).one()  # Retrieve a specific event from the database

        if myEvents.privacySetting and session["verifyCount"] == 0:
            session["eventID"] = myEvents.eventID
            return redirect(url_for("verify"))
        else:
            # create a review form object
            form = ReviewForm()
            return render_template('event.html', event=myEvents, user=session['user'], reserved=prev_res, form=form, admin=session["admin"])

    # if user is not logged in they must be redirected to login page
    else:
        return redirect(url_for("login"))


#--------------------------------------Verify User---------------------------------------#
#                verifies a user by making them log in again (Privacy Setting)           #
#----------------------------------------------------------------------------------------#
@app.route('/verify', methods=['POST', 'GET'])
def verify():
    form = LoginForm()  # Initialize to the form to the login form
    # Initial login verification; if user is logged in and saved in session
    if session.get("user"):

        #Validate the login information for a second time (Post Method)
        if form.validate_on_submit():

            # The user exists, grab that single user (Use the .one() method from DB)
            inputtedEmail = request.form["email"]   # Grab the email submitted
            inputtedPassword = request.form["password"].encode("utf-8")  # Grab the password submitted, encode it
            theUser = db.session.query(User).filter_by(email=inputtedEmail).one()

            # Check the password to see if it matches the hash stored in the database
            if bcrypt.checkpw(inputtedPassword, theUser.password):
                prev_res = db.session.query(Permission).filter_by(eventID=session["eventID"], userID=session["userID"]).count()
                myEvents = db.session.query(Event).filter_by(eventID=session["eventID"]).one()  # Retrieve a specific event from the database
                session["verifyCount"] = 1

                # The user has successfully validated their account details, return the event page with the event data stored in session data
                verifiedForm = ReviewForm()
                return render_template('event.html', event=myEvents, user=session['user'], reserved=prev_res, form=verifiedForm, admin=session["admin"])

            # The password check failed, the person logging in inputted the incorrect information
            form.password.errors = ["Incorrect username or password entered"]
            return render_template("verify.html", form=form)
        else:
            # Not a post request, it's a get method for the first time verification, render the template
            return render_template("verify.html", form=form)
    # The user is not logged in, they need to log in first to view their events. Redirect them to login.
    else:
        return redirect(url_for("login"))


#--------------------------------------get events--------------------------------------#
#                for getting all of the events                                         #
#--------------------------------------------------------------------------------------#
@app.route('/events')
def get_events():
    # login verification; if user is logged in and saved in session  
    if session.get("user"):
        sort_by = Event.eventID.desc()
        req_sort_by = request.args.get("sort")
        if req_sort_by == "alphabet":
            sort_by = Event.name.desc()
        elif req_sort_by == "start":
            sort_by = Event.dateStart.desc()
        elif req_sort_by == "capacity":
            sort_by = Event.capacity.desc()
        elif req_sort_by == "location":
            sort_by = Event.location.desc()

        myEvents = db.session.query(Event).order_by(sort_by).limit(9).all()  # Get 5 recent events from the database

        return render_template('events.html', events=myEvents, user=session['user'], admin=session["admin"], message=request.args.get("message"))  # Render the events.html page with the events gathered from the database (Array of events)
    # if user is not logged in they must be redirected to login page
    else:
        return redirect(url_for("login"))


#--------------------------------------edit event--------------------------------------#
#                for modifying an event                                                #
#--------------------------------------------------------------------------------------#
@app.route('/events_edit/<event_id>', methods = ['GET', 'POST'])
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
            image = request.files['image']
            location = request.form['location']
            capacity = request.form['capacity']
            privacySetting = request.form.get('privacySetting', False)
            event = db.session.query(Event).filter_by(eventID=event_id).one()

            filename = datetime.now().strftime("%Y%M%d%H%S") + secure_filename(image.filename)
            image.save(os.path.join("./static/img", filename))

            # update data
            event.name = name
            event.dateStart = datetime.strptime(dateStart, '%Y-%m-%dT%H:%M')
            event.dateEnd = datetime.strptime(dateEnd, '%Y-%m-%dT%H:%M')
            event.description = description
            event.location = location
            event.capacity = capacity
            event.relativePath = filename

            # Must use a comparison to "y" because if the checkbox is not checked it returns nothing (Returns Y if checked, nothing if not checked)
            event.privacySetting = privacySetting == "y"

            # updates event in db
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
            form.image.data = my_event.relativePath
            form.privacySetting.data = my_event.privacySetting

            return render_template('create_event.html', form=form, event=my_event, user=session['user'], admin=session["admin"])
    else:
        # user is not in session - redirect to login
        return redirect(url_for('login'))


#------------------------------------delete event--------------------------------------#
#                 for removing an event                                                #
#--------------------------------------------------------------------------------------#
@app.route('/events/delete/<event_id>', methods=['GET'])
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


#---------------------RSVPing to an event-----------------------------------------------#
#               Reserving a spot for an event                                           #
#---------------------------------------------------------------------------------------#
@app.route('/events/reserve/<event_id>', methods=['GET'])
def reserve_event(event_id):
    if session.get("user"):
        prev_perm = db.session.query(Permission).filter_by(eventID=event_id, userID=session["userID"])
        event = db.session.query(Event).filter_by(eventID=event_id).one()
        if prev_perm.count() == 0:
            perm = Permission(event.eventID, session["userID"], "Attendee")
            event.capacity = event.capacity - 1
            db.session.add(perm)

            # Grab the user to update the total amount of events they have joined
            theUser = db.session.query(User).filter_by(userID=session["userID"]).one()
            theUser.totalEventsJoined += 1
            db.session.commit()

        else:
            event.capacity = event.capacity + 1
            prev_perm.delete()
        db.session.commit()
        return redirect(url_for("get_event", event_id=event.eventID))
    else:
        return redirect(url_for('login'))


#---------------------get user profile--------------------------------------------------#
#               view the user's profile                                                 #
#---------------------------------------------------------------------------------------#
@app.route("/my_profile")
def get_user_profile():
    if session.get("user"):

        # Retrieve the user model to display the various stats
        userStats = db.session.query(User).filter_by(userID=session["userID"]).one()

        # Retrieve the eventID from the permission table by filtering to a specific user who is logged in and is an owner of the event.
        subqueryPermission = db.session.query(Permission.eventID).filter_by(userID=session["userID"], role="Owner").subquery()

        # Retrieve all of the events based on the subquery (The eventID from the permission table by filtering with logged in user and owner role)
        usersEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryPermission)).all()

        # Retrieve all of the events that the user has joined. Create a subquery that looks for eventIDs with the user as an attendee
        subqueryPermission2 = db.session.query(Permission.eventID).filter_by(userID=session["userID"], role="Attendee").subquery()

        # Retrieve all of the events based on the subqueryPermission2 query
        userJoinedEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryPermission2)).all()

        # Retrieve all of the reviewIDs where the user is the creator of the review
        subqueryReviews = db.session.query(Review.reviewID).filter_by(userID=session["userID"]).subquery()

        # Retrieve all of the reviews based on the subqueryReviews query ( I feel like i may have overthought this, someone else can verify and let me know (._.')  )
        userReviews = db.session.query(Review).filter(Review.reviewID.in_(subqueryReviews)).all()

        # Retrieve all of the events where the user has made a review based on the subqueryReviews
        userReviewEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryReviews)).all()

        return render_template("user_profile.html", user=session["user"], email=session["email"], admin=session["admin"], userStats=userStats, usersEvents=usersEvents, userJoinedEvents=userJoinedEvents, userReviews=userReviews, userReviewEvents=userReviewEvents)
    else:
        return redirect(url_for("login"))


#------------------------------------review event--------------------------------------#
#                 for leaving a review on an event                                     #
#--------------------------------------------------------------------------------------#
@app.route('/events/<event_id>/review', methods=['POST', 'GET'])
def new_review(event_id):
    if session.get('user'):
        event = db.session.query(Event).filter_by(eventID=event_id).one()
        review_form = ReviewForm()
        # validate_on_submit only validates using POST
        if review_form.validate_on_submit():
            # get comment data
            review_text = request.form['review']
            new_record = Review(review_text, int(event.eventID), session["userID"])
            db.session.add(new_record)
            db.session.commit()

            # Grab the user from the database to update the total amount of reviews they have made
            theUser = db.session.query(User).filter_by(userID=session["userID"]).one()
            theUser.totalEventReviews += 1
            db.session.commit()

        return redirect(url_for("get_event", event_id=event.eventID))

    else:
        return redirect(url_for('login'))


#------------------------------------Creating a user report----------------------------------------#
#                 Method for creating user reports                                                 #
#--------------------------------------------------------------------------------------------------#
def handle_report(reportID, reportType):
  tempTest = db.session.query(Report).filter_by(itemID=reportID, reportType=reportType).first()
  if tempTest is None:
    report = Report(reportID, reportType)
    db.session.add(report)
    db.session.commit()
  return redirect(url_for('get_events', message='Thank you for your report! It will be reviewed by an administrator shortly.'))


#------------------------------------Report functionality for review section-----------------------#
#                 Method for handling user reports for reviews                                     #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/review/<review_id>')
def report_review(review_id):
    return handle_report(review_id, 'review')


#------------------------------------Report functionality for events-------------------------------#
#                 Method for handling user reports for events                                      #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/event/<event_id>')
def report_event(event_id):
    return handle_report(event_id, 'event')


#------------------------------------Deleting Report for a review----------------------------------#
#                 Deletes a specified report for a review                                          #
#--------------------------------------------------------------------------------------------------#
def handle_review_report(review_id):
    reportedReview = db.session.query(Report).filter_by(reportType='review', itemID=review_id).one()
    db.session.delete(reportedReview)
    db.session.commit()
    return redirect(url_for('access_admin_panel'))


#------------------------------------Deleting Report for an event----------------------------------#
#                 Deletes a specified report for an event                                          #
#--------------------------------------------------------------------------------------------------#
def handle_event_report(event_id):
    reportedEvent = db.session.query(Report).filter_by(reportType='event', itemID=event_id).one()
    db.session.delete(reportedEvent)
    db.session.commit()
    return redirect(url_for('access_admin_panel'))


#------------------------------------Dismissing invalid action(Special)?---------------------------#
#                 Deletes a specified report for an event                                          #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/delete/review/<review_id>')
def report_delete_review(review_id):
    if not session["admin"]:
        return redirect(url_for('get_events', message='You do not have authorization to view this page'))
    deletedReview = db.session.query(Review).filter_by(reviewID=review_id).one()
    db.session.delete(deletedReview)
    db.session.commit()
    return handle_review_report(review_id)


#------------------------------------Dismissing invalid action(Delete)-----------------------------#
#                 Method for dismissing user with incorrect credentials                            #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/delete/event/<event_id>')
def report_delete_event(event_id):
    if not session["admin"]:
        return redirect(url_for('get_events', message='You do not have authorization to view this page'))
    deletedEvent = db.session.query(Event).filter_by(eventID=event_id).one()
    db.session.delete(deletedEvent)
    db.session.commit()
    return handle_event_report(event_id)


#------------------------------------Dismissing invalid action(Review)-----------------------------#
#                 Method for dismissing user with incorrect credentials                            #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/dismiss/review/<review_id>')
def report_dismiss_review(review_id):
    if not session["admin"]:
        return redirect(url_for('get_events', message='You do not have authorization to view this page'))
    return handle_review_report(review_id)


#------------------------------------Dismissing invalid action(Event)------------------------------#
#                 Method for dismissing user with incorrect credentials                            #
#--------------------------------------------------------------------------------------------------#
@app.route('/report/dismiss/event/<event_id>')
def report_dismiss_event(event_id):
    if not session["admin"]:
        return redirect(url_for('get_events', message='You do not have authorization to view this page'))
    return handle_event_report(event_id)


#------------------------------------Admin Panel Access-------------------------------------#
#                 Method for accessing the administrator panel                              #
#-------------------------------------------------------------------------------------------#
@app.route('/admin')
def access_admin_panel():
    if session["admin"] == False:
        return redirect(url_for('get_events', message='You do not have authorization to view this page'))  # need to make a custom denied page
    else:
        subqueryReview = db.session.query(Report.itemID).filter_by(reportType='review').subquery()
        reportedReviews = db.session.query(Review).filter(Review.reviewID.in_(subqueryReview)).all()

        subqueryEvent = db.session.query(Report.itemID).filter_by(reportType='event').subquery()
        reportedEvents = db.session.query(Event).filter(Event.eventID.in_(subqueryEvent)).all()
        return render_template('admin.html', user=session["user"], admin=session["admin"], events=reportedEvents, reviews=reportedReviews)


#------------------------------------change Password 1--------------------------------------#
#                 for redirecting to change password page                                   #
#-------------------------------------------------------------------------------------------#
@app.route("/my_profile/change_password", methods=['GET'])
def change_pass():
    form = PassChangeForm()  # Initialize the form object to be the register form
    return render_template('forgotPass.html', form=form)


#------------------------------------change Password 2--------------------------------------#
#                  to actually change the password                                          #
#-------------------------------------------------------------------------------------------#
@app.route("/my_profile/changed_password", methods=['POST'])
def set_pass():
    form = PassChangeForm()  # Initialize the form object to be the register form
    userid = session['userID']
    if request.method == "POST" and form.validate_on_submit():
        # Salt and Hash the password entered.
        hashedPassword = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())
        user = db.session.query(User).filter_by(userID=userid).one()
        user.password = hashedPassword

        # Add this new user object to the database
        db.session.add(user)
        db.session.commit()

        # Redirect the user 
        return redirect(url_for('get_user_profile'))
    else:
        return redirect(url_for('login'))


#--------------------------run statement------------------------------------#
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
