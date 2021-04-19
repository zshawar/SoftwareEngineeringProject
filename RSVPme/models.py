from database import db
from datetime import datetime

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
    dateStart = db.Column("dateStart", db.DateTime)
    dateEnd = db.Column("dateEnd", db.DateTime)
    location = db.Column("location", db.String(255))
    description = db.Column("description", db.VARCHAR)
    capacity = db.Column("capacity", db.Integer)
    relativePath = db.Column("relativePath", db.VARCHAR)

    # ratings are stored in two variables, rating and numRatings
    # this allows for updating the rating easily by multiplying the ratings
    # value by numRatings, add the new rating, increment numRatings, and
    # storing the new rating (rating*numRatings + newRating)/(numRatings + 1)
    rating = db.Column("rating", db.Numeric(3, 2))
    numRatings = db.Column("numRatings", db.Integer)
    permissions = db.relationship("Permission", backref="event", cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, capacity, description, location, dateStart, dateEnd, relativePath):
        self.name = name
        self.dateStart = datetime.strptime(dateStart, '%Y-%m-%dT%H:%M')
        self.dateEnd = datetime.strptime(dateEnd, '%Y-%m-%dT%H:%M')
        self.location = location
        self.description = description
        self.capacity = capacity
        self.relativePath = relativePath
        self.rating = 0
        self.numRatings = 0

class Permission(db.Model):
    eventID = db.Column("eventID", db.Integer, db.ForeignKey("event.eventID"), primary_key=True)
    userID = db.Column("userID", db.Integer, db.ForeignKey("user.userID"), primary_key=True)
    role = db.Column("role", db.String(20), db.ForeignKey("role.role"))

    def __init__(self, eventID, userID, role):
        self.eventID = eventID
        self.userID = userID
        self.role = role

class Role(db.Model):
    role = db.Column("role", db.String(20), primary_key=True)
    canViewEvent = db.Column("canViewEvent", db.Boolean)
    canViewAttendees = db.Column("canViewAttendees", db.Boolean)
    canRate = db.Column("canRate", db.Boolean)
    canRSVP = db.Column("canRSVP", db.Boolean)
    canEdit = db.Column("canEdit", db.Boolean)
    canPublish = db.Column("canPublish", db.Boolean)
    canSetPermissions = db.Column("canSetPermissions", db.Boolean)

    def __init__(self, role, canViewEvent, canViewAttendees, canRate, canRSVP, canEdit, canPublish, canSetPermissions):
        self.role = role
        self.canViewEvent = canViewEvent
        self.canViewAttendees = canViewAttendees
        self.canRate = canRate
        self.canRSVP = canRSVP
        self.canEdit = canEdit
        self.canPublish = canPublish
        self.canSetPermissions = canSetPermissions

