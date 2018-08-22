from hlint import lint

from unittest import TestCase


class TestHlint(TestCase):
    @classmethod
    def setUp(cls):
        cls.good = "input/good.html"
        cls.bad = "input/bad.html"

    def test_init(self):
        self.assertEqual(None, None)
