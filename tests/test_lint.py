import os

from hlint import lint
from unittest import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestHlint(TestCase):
    @classmethod
    def setUp(cls):
        cls.good = os.path.join(BASE_DIR, "tests/input/good.html")
        cls.bad = os.path.join(BASE_DIR, "tests/input/bad.html")

    def test_file(self):
        self.assertEqual(lint.check(self.good), True)
        self.assertEqual(lint.check(self.bad), False)
        
    def test_files(self):
        results = lint.check_files([self.good, self.bad])
        print(results)
