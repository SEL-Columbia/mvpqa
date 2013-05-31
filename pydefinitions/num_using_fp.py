import json

from bamboo.models.dataset import Dataset
from bamboo.models.observation import Observation
from bamboo.core.frame import DATASET_ID

from jinja2 import Template


class Definition(object):

    query_str = """
    {"{{dataset_id_field}}": "{{dataset.dataset_id}}",
    "{{meta_timeend}}": {
                "$gte": "{{period.start}}",
                "$lte": "{{period.end}}"
                },
    "{{num_using_fp}}": {"$gte": 0}
    }
    """
    sort_str = """
    {"$sort": {
        "{{case__case_id}}": 1,
        "{{meta_timeend}}": -1
    }}
    """
    group_str = """
    {"$group":
    {"_id": "{{case__case_id}}",
    "num_using_fp":
        {"$first": "${{num_using_fp}}"}
    }},
    {"$group":
        {"_id": null,
        "total_num_using_fp": {"$sum": "$num_using_fp"}}}
    """
    final_str = "[%s]" % u",".join(
        [u'{"$match": %s}' % query_str,
         sort_str, group_str])

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
            fields['period'] = period
            query = json.loads(Template(self.final_str).render(fields))
            meta_timeend = '%(meta_timeend)s' % fields
            query[0]['$match'][meta_timeend]['$gte'] = period.start
            query[0]['$match'][meta_timeend]['$lte'] = period.end
            aggregate_value = self._db.observations.aggregate(query)
            value = aggregate_value['result'][0]['total_num_using_fp']
        return value
