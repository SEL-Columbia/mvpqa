import json

from bamboo.models.dataset import Dataset
from bamboo.models.observation import Observation
from bamboo.core.frame import DATASET_ID

from bson.code import Code
from jinja2 import Template


class Definition(object):
    mapper_str = """
    function(){
        value = this;
        key = this['{{form_case__case_id}}'];
        if(isNaN(value["{{computed__mvp_indicators_num_antimalarials_other_value}}"])){
            value["{{computed__mvp_indicators_num_antimalarials_other_value}}"] = 0;
        }
        emit(key,  value);
    }
    """

    reducer_str = """
    function(key, values){
        values.sort(function(a, b){
            a = a["{{form_meta_timeend}}"];
            b = b["{{form_meta_timeend}}"];
            return a > b? -1: a < b? 1: 0;
        });
        var reducedValue = values[0];
        if(isNaN(reducedValue["{{computed__mvp_indicators_num_antimalarials_other_value}}"])){
            reducedValue["{{computed__mvp_indicators_num_antimalarials_other_value}}"] = 0;
        }
        return reducedValue;
    }
    """

    query_str = """
    {"{{dataset_id_field}}": "{{dataset.dataset_id}}",
    "{{doc_type}}": "XFormInstance",
    "{{form_meta_timeend}}": {
                "$gte": "{{period.start}}",
                "$lte": "{{period.end}}"
                },
    "{{computed__mvp_indicators_num_other_positive_value}}": {"$gt": 0}
    ,"{{computed__mvp_indicators_num_antimalarials_other_value}}": {"$gt": 0}
    }
    """
    aggregate_str = """
    {"$group":
    {"_id": 0, "total": {"$sum": "$value.{{computed__mvp_indicators_num_antimalarials_other_value}}"}}}
    """

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
            mapper = Code(Template(self.mapper_str).render(fields))
            reducer = Code(Template(self.reducer_str).render(fields))
            query = json.loads(Template(self.query_str).render(fields))
            query['%(form_meta_timeend)s' % fields]['$gte'] = period.start
            query['%(form_meta_timeend)s' % fields]['$lte'] = period.end
            aggregate = json.loads(Template(self.aggregate_str).render(fields))
            results = self._db.observations.map_reduce(
                mapper, reducer, 'myresults_malaria', query=query)
            value = None
            if results.count():
                aggregate_value = results.aggregate(aggregate)
                value = aggregate_value['result'][0]['total']
            self._db.myresults_malaria.drop()
        return value
