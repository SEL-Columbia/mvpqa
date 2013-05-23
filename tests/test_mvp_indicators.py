import os
import json
import unittest

from datetime import date
from mvpqa.periods import Period
from mvpqa.indicator import BambooIndicator


class TestMvpIndicator(unittest.TestCase):
    def setUp(self):
        # TODO: load fixtures to bamboo
        self.bamboo_indicator = BambooIndicator()
        self.period = Period(start=date(2013, 5, 1), end=date(2013, 6, 1))

    this_directory = os.path.dirname(__file__)

    def _load_json_indicator(self, name):
        path = os.path.join(
            self.this_directory, '..', 'definitions', '%s.json' % name)
        f = open(path)
        indicator_json = f.read()
        f.close()
        self.indicator = json.loads(indicator_json)

    def test_number_of_under_5_deaths(self):
        self._load_json_indicator('number_of_under_5_deaths')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 5)

    def test_number_of_over_5_deaths(self):
        period = Period(start=date(2013, 1, 1), end=date(2013, 6, 1))
        self._load_json_indicator('number_of_over_5_deaths')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, period)
        self.assertEqual(value, 6)

    def test_number_of_births_recorded(self):
        self._load_json_indicator('number_of_births_recorded')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 65)
