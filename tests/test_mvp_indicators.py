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
        self.period = Period.month_period(2013, 5)

    this_directory = os.path.dirname(__file__)

    def _load_json_indicator(self, name):
        path = os.path.join(
            self.this_directory, '..', 'definitions', '%s.json' % name)
        f = open(path)
        indicator_json = f.read()
        f.close()
        self.indicator = json.loads(indicator_json)
        self.assertEqual(
            self.indicator['name'], name)

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

    def test_number_of_infant_deaths_0_to_11_months(self):
        self._load_json_indicator('number_of_infant_deaths_0_to_11_months')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 5)

    def test_number_of_neonatal_deaths_0_to_28_days(self):
        self._load_json_indicator('number_of_neonatal_deaths_0_to_28_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 4)

    def test_number_of_maternal_deaths(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('number_of_maternal_deaths')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 1)

    def test_proportion_of_households_receiving_on_time_visits_last_90(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_households_receiving_on_'
                                  'time_routine_visits_last_90_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 64.37)

    def test_proportion_of_households_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_households_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 41.67)

    def test_proportion_of_under5_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 40.61)

    def test_proportion_of_pregnant_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_pregnant_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 60.61)

    def test_proportion_of_newborns_receiving_on_time_visits_7days(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_newborns_receiving_1st_chw_'
                                  'checkup_within_7_days_of_birth')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, 9.57)
