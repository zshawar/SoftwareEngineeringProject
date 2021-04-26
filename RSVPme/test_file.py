import unittest
import requests
from models import User
from database import db

class FlaskTest(unittest.TestCase):

    # create mock user
    mockUser = User(userName='username', email='email@email.com', hashedPassword='12345')
    # Add this mock user object to the database
    db.session.add(mockUser)
    db.session.commit()

    def test_home(self):
        response = requests.get("http://127.0.0.1:5000/home")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Welcome to RSVMe!' in response.text, True)

    def test_register(self):
        response = requests.get("http://127.0.0.1:5000/register")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Fill out the form below to create your account!' in response.text, True)

    def test_public_events(self):
        response = requests.get("http://127.0.0.1:5000/events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Reserve my Spot!' in response.text, True)

    def test_my_events(self):
        response = requests.get("http://127.0.0.1:5000/my_events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Joined Events' in response.text, True)

    def test_create_event(self):
        response = requests.get("http://127.0.0.1:5000/events/create")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Start Date and Time' in response.text, True)

    #def test_delete_event(self):

if __name__ == " __main__":
    unittest.main()
