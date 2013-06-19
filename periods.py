from datetime import datetime
from dateutil.relativedelta import relativedelta


def datetimeformat(value, format='%Y-%m-%d'):
        return value.strftime(format)


class Period(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def month_period(cls, year, month):
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(
            day=31, hour=23, minute=59, second=59, microsecond=999999)
        return cls(start_date, end_date)

    @property
    def ninety_days_before_end_of_period(self):
        """Returns date ninety days before the periods end"""
        return self.end + relativedelta(days=-90)

    @property
    def thirty_days_before_end_of_period(self):
        """Returns date thirty days before the periods end"""
        return self.end + relativedelta(days=-30)
   
    @property
    def six_weeks_before_end_of_period(self):
        """Returns date 42 days before the periods end"""
        return self.end + relativedelta(days=-42)

    @property
    def five_years_before_end_of_period(self):
        """Returns date five years before the periods end"""
        return self.end + relativedelta(days=-1825)

    @property
    def six_months_before_end_of_period(self):
        """Returns date six months before the periods end"""
        return self.end + relativedelta(days=-180)

    @property
    def seven_days_before_end_of_period(self):
        """Returns seven days before the periods end"""
        return self.end + relativedelta(days=-7)

    @property
    def one_year_before_end_of_period(self):
        """Returns one year before the periods end"""
        return self.end + relativedelta(days=-365)
