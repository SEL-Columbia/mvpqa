import json
import sys
import os

from bamboo.models.dataset import Dataset
from bamboo.models.observation import Observation
from bamboo.core.frame import DATASET_ID

from jinja2 import Template

sys.path.append(
    os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
)
from mvpqa.periods import Period


class Definition(object):

    query_str = """
    {"{{dataset_id_field}}": "{{dataset.dataset_id}}",
    "{{meta_timeend}}": {
                "$gte": "{{period.start}}",
                "$lte": "{{period.end}}"
                },
    "{{num_other_positive}}": {"$gt": 0},
    "{{num_rdt_other}}": {"$gt": 0}
    }
    """
    project_str = """
    {"$project": {
        "{{num_other_positive}}": 1,
        "{{num_rdt_other}}": 1
    }}
    """
    aggregate_str = """
    {"$group":
    {"_id": 0, "total_num_rdt_other":
        {"$sum": "${{num_rdt_other}}"},
    "total_num_other_positive": {"$sum": "${{num_other_positive}}"}
    }}
    """
    project_str2 = """
    {"$project":
        {"total_difference":
            {"$subtract":
                ["$total_num_rdt_other", "$total_num_other_positive"]}}}
    """
    final_str = "[%s]" % u",".join(
        [u'{"$match": %s}' % query_str,
         project_str, aggregate_str, project_str2])

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
        if self.dataset:
            fields = Observation.encoding(self.dataset)
            fields["dataset"] = self.dataset
            fields['dataset_id_field'] = fields[DATASET_ID]
            fields['period'] = Period.month_period(2013, 3)
            query = json.loads(Template(self.final_str).render(fields))
            meta_timeend = '%(meta_timeend)s' % fields
            query[0]['$match'][meta_timeend]['$gte'] = period.start
            query[0]['$match'][meta_timeend]['$lte'] = period.end
            aggregate_value = self._db.observations.aggregate(query)
            value = aggregate_value['result'][0]['total_difference']
        return value
