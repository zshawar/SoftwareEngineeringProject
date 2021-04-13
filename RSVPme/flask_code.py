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

