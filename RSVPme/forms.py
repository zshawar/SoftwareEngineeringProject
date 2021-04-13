from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, ValidationError
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

    # need to write function to validate user login

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

    # need to write function to validate user login

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

    # stub, missing some fields

