from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, DateTimeField, ValidationError
from wtforms.validators import Length, DataRequired, EqualTo, Email

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

    eventName = StringField("EventName", [
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
    image = FileField("Event Thumbnail", [])

    capacity = IntegerField("Capacity", [])

    dateStart = DateTimeField("Start Date and Time", [])
    dateEnd = DateTimeField("End Date and Time", [])

    

