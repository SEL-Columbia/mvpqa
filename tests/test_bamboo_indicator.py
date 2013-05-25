import os
import json
import unittest

from datetime import date
from mvpqa.periods import Period
from mvpqa.indicator import BambooIndicator


class TestBambooIndicator(unittest.TestCase):
    def setUp(self):
        self.bamboo_indicator = BambooIndicator()
        self.period = Period(start=date(2013, 5, 1), end=date(2013, 6, 1))

    this_directory = os.path.dirname(__file__)

    def _load_json_indicator(self, name):
        path = os.path.join(
            self.this_directory, 'fixtures', '%s.json' % name)
        f = open(path)
        indicator_json = f.read()
        f.close()
        self.indicator = json.loads(indicator_json)

    def test_get_value(self):
        self._load_json_indicator('indicator')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 5)

    #Test if proportion work using
    # Denominator: number_of_births_recorded = 65
    # Numerator: number_of_under_5_deaths = 5
    def test_proportions(self):
        self._load_json_indicator('proportions')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value['denominator'], 65)
        self.assertEqual(value['numerator'], 5)
