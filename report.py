import os
import sys
import csv
import json

sys.path.append(os.getcwd())

from indicator import BambooIndicator
from periods import Period


SRC_DIR = os.path.dirname(__file__)
DEFINITIONS_DIR = os.path.join(
    SRC_DIR, 'definitions'
)


def _get_indicator_definitions(indicator_name=None):
    INDICATOR_DEFS = []
    if isinstance(indicator_name, basestring):
        full_path = os.path.join(DEFINITIONS_DIR, '%s.json' % indicator_name)
        with open(full_path) as f:
            obj = json.load(f)
            INDICATOR_DEFS.append(obj)
        return INDICATOR_DEFS

    for filename in os.listdir(DEFINITIONS_DIR):
        if filename.endswith('.json'):
            full_path = os.path.join(DEFINITIONS_DIR, filename)
            with open(full_path) as f:
                try:
                    obj = json.load(f)
                except:
                    # TODO: appropriate feedback, handle this somehow
                    pass
                else:
                    INDICATOR_DEFS.append(obj)
    return sorted(INDICATOR_DEFS, key=lambda k: k['type'])


def _generate_indicator_export(name, period, indicator_name=None):
    INDICATOR_DEFS = _get_indicator_definitions(indicator_name)

    bi = BambooIndicator()
    RESULTS = [
        (u"MVP Indicators For The Period: %(start)s - %(end)s" % {
            'start': period.start.strftime('%Y-%m-%d'),
            'end': period.end.strftime('%Y-%m-%d'),
        },),
        (u"Indicator Type", u"Indicator", u"Value",
            u"Numerator", u"Denominator")
    ]
    for indicator_def in INDICATOR_DEFS:
        value = denominator = numerator = None
        value, numerator, denominator = \
            bi.get_indicator_value(indicator_def, period)
        RESULTS.append(
            (indicator_def['type'], indicator_def['description'],
                value, numerator, denominator))
        print (indicator_def['type'], indicator_def['name'],
               value, numerator, denominator)

    filename = "%(name)s_mvp_indicator_%(start)s_to_%(end)s.csv" % {
        'name': name,
        'start': period.start.strftime('%Y-%m-%d'),
        'end': period.end.strftime('%Y-%m-%d')}
    with open(filename, 'wb') as f:
        csv_writer = csv.writer(
            f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(RESULTS)

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) < 3:
        print (u"Expected site_name YEAR MONTH\n"
               u"Eg.\n\t python report.py ruhiira 2013 03")
    else:
        name = arguments[0]
        year = int(arguments[1])
        month = int(arguments[2])
        period = Period.month_period(year, month)
        indicator = None
        if arguments.__len__() > 3:
            indicator_name = arguments[3]
        _generate_indicator_export(name, period, indicator_name)
