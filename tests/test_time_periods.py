import unittest

from datetime import datetime

from mvpqa.periods import Period


class TestTimePeriod(unittest.TestCase):
    def test_time_period(self):
        start_date = datetime(2013, 05, 01)
        end_date = datetime(2013, 05, 31)
        period = Period(start_date, end_date)
        self.assertEqual(period.start, start_date)
        self.assertEqual(period.end, end_date)

    def test_month_period(self):
        period = Period.month_period(2013, 05)
        self.assertEqual(period.start, datetime(2013, 05, 1))
        self.assertEqual(
            period.end, datetime(2013, 05, 31, 23, 59, 59, 999999))
