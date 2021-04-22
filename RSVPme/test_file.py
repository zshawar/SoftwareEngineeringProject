import unittest
import requests

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
        self.assertEqual('Username' in response.text, True)

    def test_public_events(self):
        response = requests.get("http://127.0.0.1:5000/events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Reserve my Spot!' in response.text, True)

    def test_my_events(self):
        response = requests.get("http://127.0.0.1:5000/my_events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('My Events' in response.text, True)

    def test_create_event(self):
        response = requests.get("http://127.0.0.1:5000/events/create")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Start Date and Time' in response.text, True)

    #def test_delete_event(self):

if __name__ == " __main__":
    unittest.main()
