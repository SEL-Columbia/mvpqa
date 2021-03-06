import sys
import os

from bamboo.models.dataset import Dataset

sys.path.append(
    os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
)
from mvpqa.pydefinitions import num_bednets_observed
from mvpqa.pydefinitions import num_sleeping_sites


class Definition(object):
    def __init__(self, db, dataset_id=None, dataset=None):
        self._db = db
        if dataset_id:
            self.dataset = Dataset.find_one(dataset_id)
        if dataset:
            self.dataset = dataset
        if not dataset_id and not dataset:
            raise Exception(u"Please specify a dataset_id")

    def get_value(self, period):
        value = None
        def1 = num_bednets_observed.Definition(
            self._db, dataset=self.dataset)
        numerator = def1.get_value(period)
        def2 = num_sleeping_sites.Definition(
            self._db, dataset=self.dataset)
        denominator = def2.get_value(period)
        if denominator == 0:
            value = 0
        else:
            value = round(100 * (float(numerator) / float(denominator)), 2)
        return value, numerator, denominator
