import json

from bamboo.models.dataset import Dataset
from bamboo.models.observation import Observation
from bamboo.core.frame import DATASET_ID

from jinja2 import Template


class Definition(object):

    query_str = """
    {"{{dataset_id_field}}": "{{dataset.dataset_id}}",
    "{{doc_type}}": "XFormInstance",
    "{{form_meta_timeend}}": {
                "$gte": "{{period.start}}",
                "$lte": "{{period.end}}"
                },
    "{{computed__mvp_indicators_num_other_positive_value}}": {"$gt": 0},
    "{{server_computed__mvp_indicators_num_antimalarials_other_value}}": {"$gt": 0}
    }
    """
    project_str = """
    {"$project": {
        "{{computed__mvp_indicators_num_other_positive_value}}": 1,
        "{{server_computed__mvp_indicators_num_antimalarials_other_value}}": 1
    }}
    """
    aggregate_str = """
    {"$group":
    {"_id": 0, "total_num_antimalarials":
        {"$sum": "${{server_computed__mvp_indicators_num_antimalarials_other_value}}"},
    "total_num_other_positive": {"$sum": "${{computed__mvp_indicators_num_other_positive_value}}"}
    }}
    """
    project_str2 = """
    {"$project":
        {"total_difference":
            {"$subtract":
                ["$total_num_antimalarials", "$total_num_other_positive"]}}}
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
            fields['period'] = period
            query = json.loads(Template(self.final_str).render(fields))
            form_meta_timeend = '%(form_meta_timeend)s' % fields
            query[0]['$match'][form_meta_timeend]['$gte'] = period.start
            query[0]['$match'][form_meta_timeend]['$lte'] = period.end
            aggregate_value = self._db.observations.aggregate(query)
            value = aggregate_value['result'][0]['total_difference']
        return value
