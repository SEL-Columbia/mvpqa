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
        self.assertEqual(value, (5, None, None))

    def test_number_of_over_5_deaths(self):
        period = Period(start=date(2013, 1, 1), end=date(2013, 6, 1))
        self._load_json_indicator('number_of_over_5_deaths')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, period)
        self.assertEqual(value, (6, None, None))

    def test_number_of_births_recorded(self):
        self._load_json_indicator('number_of_births_recorded')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (65, None, None))

    def test_number_of_infant_deaths_0_to_11_months(self):
        self._load_json_indicator('number_of_infant_deaths_0_to_11_months')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (5, None, None))

    def test_number_of_neonatal_deaths_0_to_28_days(self):
        self._load_json_indicator('number_of_neonatal_deaths_0_to_28_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (4, None, None))

    def test_number_of_maternal_deaths(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('number_of_maternal_deaths')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (1, None, None))

    def test_proportion_of_households_receiving_on_time_visits_last_90(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_households_receiving_on_'
                                  'time_routine_visits_last_90_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (64.37, 7984, 12403))

    def test_proportion_of_households_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_households_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (41.67, 4458, 10699))

    def test_proportion_of_under5_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (40.61, 4392, 10815))

    def test_proportion_of_pregnant_receiving_on_time_visits_last_30(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_pregnant_receiving_on_'
                                  'time_routine_visits_last_30_days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (60.61, 437, 721))

    def test_proportion_of_newborns_receiving_on_time_visits_7days(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_newborns_receiving_1st_chw_'
                                  'checkup_within_7_days_of_birth')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (9.57, 69, 721))

    def test_proportion_of_neonates_receiving_on_time_visits_7days(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_neonates_receiving'
                                  '_on_time_routine_visit_within_7days')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0.8, 87, 10815))

    def test_proportion_of_low_birth_weight_babies(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_low_birth_weight_babies')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (1.05, 1, 95))

    def test_proportion_of_under5_with_uncomplicated_diarrhea_got_ors(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_uncomplicated'
                                  '_diarrhea_received_ors')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (92.74, 166, 179))

    def test_proportion_of_under5_with_uncomplicated_diarrhea_got_zinc(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_uncomplicated'
                                  '_diarrhea_received_zinc')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (91.06, 163, 179))

    def test_proportion_of_pregnant_routine_checkup_6weeks(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_pregnant_routine_checkup_'
                                  '6weeks')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0.0, 0, 792))

    def test_proportion_of_birth_health_facility(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_birth_health_facility')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0.0, 0, 115))

    def test_proportion_of_pregnant_reporting_anc_4months(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_pregnant_reporting_anc'
                                  '_4months')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0, 0, 0))

    def test_proportion_of_under5_with_positive_rdt_received_adt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_positive_rdt_'
                                  'received_adt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (93.02, 40, 43))

    def test_proportion_of_under5_with_uncomplecated_fever_received_rdt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_uncomplecated_'
                                  'fever_received_rdt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (100.0, 153, 153))

    def test_proportion_of_u5_with_uncmpl_fever_received_rdt_positive(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_uncomplecated_'
                                  'fever_received_rdt_positive')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (28.1, 43, 153))

    def test_proportion_of_under5_with_uncomplecated_fever_no_rdt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_uncomplecated_'
                                  'fever_no_rdt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0.0, 0, 153))

    def test_proportion_of_under5_with_negative_rdt_received_adt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_under5_with_negative_rdt_'
                                  'received_adt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (0.0, 0, 110))

    def test_proportion_of_over5_with_positive_rdt_receiving_adt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_over5_with_positive_rdt_'
                                  'received_adt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (130.23, 112.0, 86.0))

    def test_proportion_of_over5_with_negative_rdt_receiving_adt(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_over5_with_negative_rdt_'
                                  'received_adt')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (-25.0, -1.0, 4.0))

    def test_proportion_of_women_using_modern_fp(self):
        self.period = Period.month_period(2013, 3)
        self._load_json_indicator('proportion_of_women_using_modern_fp')
        value = self.bamboo_indicator\
            .get_indicator_value(self.indicator, self.period)
        self.assertEqual(value, (100.0, 1.0, 1.0))
