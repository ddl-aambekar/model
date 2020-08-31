from unittest import TestCase

import model

class TestJoke(TestCase):
    def test_is_dict(self):
        s = model.my_model(1,100)
        print(s)
        self.assertTrue(isinstance(s, dict))

    def test_is_inRange(self):
        s = model.my_model(1,100)
        self.assertTrue(s, dict)