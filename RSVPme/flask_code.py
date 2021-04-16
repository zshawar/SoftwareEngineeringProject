#--------------------------import statements----------------------------------#
import os                 
from flask import Flask   
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from forms import LoginForm, RegisterForm, EventForm
from models import User, Event, Role, Permission



#--------------------------setup----------------------------------------------#
app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rsvpme.db' #temporarily commented out --- need add db for it to work

db.init_app(app)

with app.app_context():
    db.create_all()   # run under the app context

#----------------------------home page---------------------------------------#
@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    
    #your code here
    return render_template("home.html") # may need to add paramaters

#----------------------------login functionality---------------------------------------#
@app.route('/home/user_login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        #stuff for if they hit 'click to login'
    #More may be needed
        return redirect(url_for('home'))
    else:
        return render_template("login.html", form=LoginForm) # may need to add parameters

#----------------------------register functionality---------------------------------------#
@app.route('/home/user_login/register_user')
def register():
    #your code here
    return render_template("register.html", form=RegisterForm) # may need to add parameters
    ###########return this if they successfully register###########
    # else:
    #     return redirect(url_for('login')) #may need parameters

#----------------------------add event functionality---------------------------------------#
@app.route('/events/create')
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        dateofEvent = request.form['dateofEvent']
        description = request.form['description']
        location = request.form['location']
        capacity = request.form['capacity']
        
        newEvent = Event(name, Event, description, location, capacity)
        db.session.add(newEvent)
        db.session.commit()

        return redirect(url_for('get_events'))
    else:
        return render_template('modify_event.html')


#-----------------------------my events page-------------------------------------------#
@app.route('/my_events', methods=['GET'])
def get_user_events(user_id):
     #**********************add code to re-verify login here*************************#


    return render_template("my_events.html") # may need to add paramaters




#--------------------------------------get event---------------------------------------#
#                for very specifically showing one event in particular                 #
#--------------------------------------------------------------------------------------#
@app.route('/events/<event_id>')
def get_event(event_id):
    #**********************add code to re-verify login here*************************#

    myEvents = db.session.query(Event).filter_by(id=event_id).one()  # Retrieve a specific event from the database




    return render_template('event.html', event=myEvents)


#--------------------------------------get events--------------------------------------#
#                for getting all of the events                                         #
#--------------------------------------------------------------------------------------#
@app.route('/events')
def get_events():

    #**********************add code to re-verify login here*************************#

    dictionary = {1: {
        "name" : "bruh1"
        }
    }


    array = [dictionary]



    #myEvents = db.session.query(Event).limit(9).all()  # Get 5 recent events from the database

    return render_template('events.html', events=array)  # Render the events.html page with the events gathered from the database (Array of events)


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
