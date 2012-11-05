from flask.ext.testing import TestCase
import unittest

from app import app
import string


class MyTest(TestCase):
    TESTING = True
    testStrings = [ "to", "of", "the", "I", "a", "have", "for", "in", "that", "anyone", "me", "be", "it", "on",
     "you", "my", "at", "or", "To", "Sent", "Thanks", "Olin", "would", "is", "if", "need", "can", "Does", "Of", 
     "know", "could", "Behalf", "ride", "was", "willing", "how", "so", "out", "will", "like", "has", "It", "your"] + [c for c in string.printable]

    def create_app(self):
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict(self):
        for word in self.testStrings:
            response = self.client.get("/?query=%s"%word)
            if "Well, that didn't go quite as planned." in response.data:
                return False

if __name__ == '__main__':
    unittest.main()

