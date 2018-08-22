from hlint import Linter

from unittest import main as test_main, TestCase

class TestHlint(TestCase):
    @classmethod
    def setUp(cls):
        cls.good = "input/good.html"
        cls.bad = "input/bad.html"
        
    def test_init(self):
        l = Linter()
        self.assertNotEqual(l, None)
