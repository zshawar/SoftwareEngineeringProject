import unittest
import requests
from models import User
from database import db

class FlaskTest(unittest.TestCase):

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
        self.assertEqual('Public Events - Click To View' in response.text, True)

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

    def test_my_profile(self):
        response = requests.get("http://127.0.0.1:5000/my_profile")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Username' and 'Email' in response.text, True)

    def test_change_password(self):
        response = requests.get("http://127.0.0.1:5000/my_profile/change_password")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Submit' in response.text, True)





if __name__ == " __main__":
    unittest.main()
