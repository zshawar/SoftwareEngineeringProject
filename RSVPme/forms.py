import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from database import db
from models import User

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField("Email", [
        Email(),
        DataRequired()
    ])

    password = PasswordField("Password", [
        DataRequired()
    ])

    submit = SubmitField("Submit")

    def validate_password(self, field):
        users = db.session.query(User).filter_by(email=self.email.data)
        if users.count() == 0:
            raise ValidationError("Incorrect username or password")

        # we know the email exists, check the password now
        user = users.one()
        if not bcrypt.checkpw(self.password.data.encode("utf-8"), user.password):
            raise ValidationError("Incorrect username or password")


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", [
        DataRequired(),
        Length(5, 20)
    ])
    
    email = StringField("Email", [
        Email(),
        DataRequired()
    ])

    password = PasswordField("Password", [
        # work out what exactly should be required
    ])

    submit = SubmitField("Submit")


class EventForm(FlaskForm):
    class Meta:
        csrf = False

    eventName = StringField("Event Name", [
        DataRequired(),
        Length(1, 50)
    ])

    description = StringField("Description", [
        DataRequired(),
        Length(min=1)
    ])

    location = StringField("Location", [
        DataRequired(),
        Length(min=1)
    ])

    # incomplete, need to add validators for image extension
    image = FileField("Event Thumbnail", [Regexp(".*\\.(jpg|jpeg|png)$")])

    capacity = IntegerField("Capacity", [DataRequired()])

    dateStart = DateTimeLocalField("Start Date and Time", [DataRequired()], format='%Y-%m-%dT%H:%M')
    dateEnd = DateTimeLocalField("End Date and Time", [DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Submit")
    

