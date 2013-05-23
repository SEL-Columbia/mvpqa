from datetime import datetime
from dateutil.relativedelta import relativedelta


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
