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
        """Tests one file at a time"""
        result = lint.check(self.good)
        self.assertEqual(result.flag, True)

        result = lint.check(self.bad)
        self.assertEqual(result.flag, False)

    def test_files(self):
        """Tests batch files"""
        results = lint.check_files([self.good, self.bad])
        self.assertEqual(results.total_error_count, 1)
