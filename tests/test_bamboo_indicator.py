import os
import json
import unittest

from datetime import date
from mvpqa.periods import Period
from mvpqa.indicator import BambooIndicator


class TestBambooIndicator(unittest.TestCase):
    def setUp(self):
        self.bamboo_indicator = BambooIndicator()
        self._load_json_indicator()

    this_directory = os.path.dirname(__file__)

    def _load_json_indicator(self):
        path = os.path.join(self.this_directory, 'fixtures', 'indicator.json')
        f = open(path)
        indicator_json = f.read()
        f.close()
        self.indicator = json.loads(indicator_json)

    def test_get_value(self):
        period = Period(start=date(2013, 5, 1), end=date(2013, 6, 1))
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, period)
        self.assertEqual(value, 5)
