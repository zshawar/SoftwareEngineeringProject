#--------------------------import statements----------------------------------#
import os                 
from flask import Flask   
from flask import render_template
from flask import request
from flask import redirect, url_for 

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







#--------------------------run statement------------------------------------#
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True) 	#this is directly from class so see if we need to change anything?