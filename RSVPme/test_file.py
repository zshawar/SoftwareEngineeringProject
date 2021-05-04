import unittest
import requests
from models import User
from database import db

class FlaskTest(unittest.TestCase):

#  The event ID of an event or review ID is the order in which it was created.
#  The review ID (needed for reporting reviews) would be 1 for the first review,
#  2 for the second review, etc. The first event or review’s details will be located
#  at “/events/1” or “/reviews/1”, the second event’s details will be displayed at
#  “/events/2” and so on.

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

    def test_modify_event(self):
        response = requests.get("http://127.0.0.1:5000/events_edit/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Edit Event' in response.text, True)

    def test_delete_events(self):
        response = requests.get("http://127.0.0.1:5000/events/delete/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

    def test_reserve_event(self):
        response = requests.get("http://127.0.0.1:5000/events/reserve/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Cancel my Reservation' in response.text, True)

    def test_add_review(self):
        response = requests.get("http://127.0.0.1:5000/events/<event_id>/review")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Reviews' in response.text, True)

    def test_report_review(self):
        response = requests.get("http://127.0.0.1:5000/report/review/<review_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Thank you for your report! It will be reviewed by an administrator shortly.' in response.text, True)

    def test_report_event(self):
        response = requests.get("http://127.0.0.1:5000/report/event/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Thank you for your report! It will be reviewed by an administrator shortly.' in response.text, True)

    def test_sort_location(self):
        response = requests.get("http://127.0.0.1:5000/events?sort=location")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Public Events - Click To View' in response.text, True)

    # administrators are able to do this only; administrators must be set in database before running project
    def test_delete_review_report(self):
        response = requests.get("http://127.0.0.1:5000/report/delete/review/<review_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('You do not have authorization to view this page' in response.text, True)

    # administrators are able to do this only; administrators must be set in database before running project
    def test_delete_event_report(self):
        response = requests.get("http://127.0.0.1:5000/report/delete/event/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('You do not have authorization to view this page' in response.text, True)

    # administrators are able to do this only; administrators must be set in database before running project
    def test_admin(self):
        response = requests.get("http://127.0.0.1:5000/admin")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('You do not have authorization to view this page' in response.text, True)

    # administrators are able to do this only; administrators must be set in database before running project
    def test_dismiss_review_report(self):
        response = requests.get("http://127.0.0.1:5000/report/dismiss/review/<review_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('You do not have authorization to view this page' in response.text, True)

    # administrators are able to do this only; administrators must be set in database before running project
    def test_dismiss_event_report(self):
        response = requests.get("http://127.0.0.1:5000/report/dismiss/event/<event_id>")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('You do not have authorization to view this page' in response.text, True)

if __name__ == " __main__":
    unittest.main()
