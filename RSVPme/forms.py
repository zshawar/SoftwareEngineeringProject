import bcrypt
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, FileField, SubmitField, IntegerField, ValidationError, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from database import db
from models import User

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField("Email", [
        Email(message="Not a valid email address"),
        DataRequired(message="Please enter an email.")
    ])

    password = PasswordField("Password", [
        DataRequired(message="Please enter a password.")
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
        DataRequired(message="Please enter a username."),
        Length(5, 20)
    ])
    
    email = StringField("Email", [
        Email(message="Not a valid email address"),
        DataRequired(message="Please enter an email address")
    ])

    password = PasswordField("Password", [
        DataRequired(message="Please enter a password."),
        Length(5, 20)
    ])

    submit = SubmitField("Submit")

    def validateEmail(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already registered.')

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
    image = FileField("Event Thumbnail", [FileRequired(), FileAllowed(["jpg", "jpeg", "png"], "Only images are allowed")])

    capacity = IntegerField("Capacity", [DataRequired()])

    dateStart = DateTimeLocalField("Start Date and Time", [DataRequired()], format='%Y-%m-%dT%H:%M')
    dateEnd = DateTimeLocalField("End Date and Time", [DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Submit")
    
class ReviewForm(FlaskForm):
    class Meta:
        csrf = False

    review = TextAreaField('Review', validators=[Length(min=1)])

    submit = SubmitField('Add Review')
