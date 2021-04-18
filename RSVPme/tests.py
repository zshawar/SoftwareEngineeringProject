import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_home(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<title>RSVPme Home</title>' in response.text, True)

    def test_

if __name__ == " __main__":
    unittest.main()