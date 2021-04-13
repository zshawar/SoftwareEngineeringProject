from database import db

class User(db.Model):
    userID = db.Column("userID", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20))
    email = db.Column("email", db.String(30))
    password = db.Column("password", db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Event(db.Model):
    eventID = db.Column("eventID", db.Integer, primary_key=True)
    name = db.Column("name", db.String(255))
    dateAndTime = db.Column("dateOfEvent", db.DateTime)
    location = db.Column("location", db.String(255))
    description = db.Column("description", db.VARCHAR)

    # ratings are stored in two variables, rating and numRatings
    # this allows for updating the rating easily by multiplying the ratings
    # value by numRatings, add the new rating, increment numRatings, and
    # storing the new rating (rating*numRatings + newRating)/(numRatings + 1)
    rating = db.Column("rating", db.Numeric(3, 2))
    numRatings = db.Column("numRatings", db.Integer)


