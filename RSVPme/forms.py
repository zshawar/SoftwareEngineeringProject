import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, DateTimeField, ValidationError
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from database import db

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
        user = user.one()
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
    image = FileField("Event Thumbnail", [Regexp(".*\\.(jpg|jpeg|png)$")])

    capacity = IntegerField("Capacity", [])

    dateStart = DateTimeField("Start Date and Time", [])
    dateEnd = DateTimeField("End Date and Time", [])

    

