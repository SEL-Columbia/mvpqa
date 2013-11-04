import sys
import os

sys.path.append(
    os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
)


class Definition(object):
    def __init__(self, db, dataset_id=None, dataset=None):
        pass

    def get_value(self, period):
        return None, None, None
