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
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rsvpme.db' #temporarily commented out --- need add db for it to work

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
@app.route('home/user_login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        #stuff for if they hit 'click to login'
    #More may be needed
        return redirect(url_for('home')
    else:
        return render_template("login.html", form=LoginForm) # may need to add paramaters

#----------------------------register functionality---------------------------------------#
@app.route('home/user_login/register_user')
def register():
    #your code here
    return render_template("register.html", form=RegisterForm) # may need to add paramaters
    ###########return this if they succesfully register###########
    # else:
    #     return redirect(url_for('login')) #may need parmaeters

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
@app.route('/home/my_events', methods=['GET'])
def get_user_events(user_id):
    
    #your code here
    return render_template("my_events.html") # may need to add paramaters

#-------------------------------------------------------edit functionality -----------------------------------------------------------#

@app.route('home/events/edit/<event_id>', methods = ['GET', 'POST'])		#most of this is commented out and will be fixed later once we know what feilds are needed and what they are called specificaly
def modify_event(event_id):
	#check method used for request
	if request.method == 'POST':
		#**********************add code to re-verify login here*************************#
        name = request.form['name']	
        dateofEvent = request.form['dateofEvent']
        description = request.form['description']
        location = request.form['location']
        capacity = request.form['capacity']
        
        event = db.session.query(Event).filter_by(id=event_id).one()
		
		event.name = name
		event.dateofEvent = dateofEvent
        event.description = description
        event.name = location
        event.capacity = capacity
        		
		db.session.add(event)
		db.session.commit()

		return redirect(url_for('get_user_events'))
	#else: #the usual code 
		#retrieve user and note from database
		#a_user = db.session.query(User).filter_by(user_id= <id here>).one()
		#my_note = db.session.query(Event).filter_by(id=event_id).one()

		#return render_template('new.html') #add parameters as needed

#--------------------------------------------delete functionality---------------------------------------------------------------#

#@app.route('/events/delete/<event_id>', methods=['POST'])	#most of this is commented out and will be fixed later once we know what feilds are needed and what they are called specificaly
#def delete_event(event_id):
#	my_event = db.session.query(Event).filter_by(id=event_id).one()
	#**********************add code to re-verify login here*************************#
#	db.session.delete(my_event) #change the name for this var as needed
#	db.session.commit()

#	return redirect(url_for('get_events'))




#--------------------------run statement------------------------------------#
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True) 	#this is directly from class so see if we need to change anything?