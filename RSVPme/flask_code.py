#--------------------------import statements----------------------------------#
import os                 
from flask import Flask   
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from forms import LoginForm, RegisterForm, EventForm
from models import User
from models import Event
from models import Role
#--------------------------setup----------------------------------------------#
app = Flask(__name__)     # create an app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rsvpme.db' #temporarily commented out --- need add db for it to work

db.init_app(app)

with app.app_context():
    db.create_all()   # run under the app context

#----------------------------home page---------------------------------------#
@app.route('/')
@app.route('/home')
def home():
    #your code here
    return render_template("home.html") # may need to add paramaters

#----------------------------login functionality---------------------------------------#
@app.route('/login')
def login():
    #your code here
    return render_template("login.html", form=LoginForm) # may need to add paramaters

#----------------------------register functionality---------------------------------------#
@app.route('/register')
def register():
    #your code here
    return render_template("register.html", form=RegisterForm) # may need to add paramaters

#----------------------------add event functionality---------------------------------------#
@app.route('/events/createEvent')
def create_event():
    #your code here
    return render_template("create_event.html", form=EventForm) # may need to add paramaters

#-------------------------------------------------------edit functionality -----------------------------------------------------------#

#@app.route('/events/edit/<event_id>', methods = ['GET', 'POST'])		#most of this is commented out and will be fixed later once we know what feilds are needed and what they are called specificaly
#def update_event(event_id):
	#check method used for request
	#if request.method == 'POST':
		#**********************add code to re-verify login here*************************#
		#title = request.form['title']	#request title
		#text = request.form['noteText']
		#note = db.session.query(Event).filter_by(id=event_id).one()
		
		#note.title = title
		#note.text = text #updates note data
		
		#db.session.add(event)#update db
		#db.session.commit()

		#return redirect(url_for('get_events'))
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