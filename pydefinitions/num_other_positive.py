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
        key = this['{{case__case_id}}'];
        if(isNaN(value["{{num_other_positive}}"])){
            value["{{num_other_positive}}"] = 0;
        }
        emit(key,  value);
    }
    """

    reducer_str = """
    function(key, values){
        values.sort(function(a, b){
            a = a["{{meta_timeend}}"];
            b = b["{{meta_timeend}}"];
            return a > b? -1: a < b? 1: 0;
        });
        var reducedValue = values[0];
        if(isNaN(reducedValue["{{num_other_positive}}"])){
            reducedValue["{{num_other_positive}}"] = 0;
        }
        return reducedValue;
    }
    """

    query_str = """
    {"{{dataset_id_field}}": "{{dataset.dataset_id}}",
    "{{meta_timeend}}": {
                "$gte": "{{period.start}}",
                "$lte": "{{period.end}}"
                },
    "{{num_other_positive}}": {"$gt": 0}
    }
    """
    aggregate_str = """
    {"$group": {"_id": 0, "total": {"$sum": "$value.{{num_other_positive}}"}}}
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
            query['%(meta_timeend)s' % fields]['$gte'] = period.start
            query['%(meta_timeend)s' % fields]['$lte'] = period.end
            aggregate = json.loads(Template(self.aggregate_str).render(fields))
            results = self._db.observations.map_reduce(
                mapper, reducer, 'myresults_malaria', query=query)
            value = None
            if results.count():
                aggregate_value = results.aggregate(aggregate)
                value = aggregate_value['result'][0]['total']
            self._db.myresults_malaria.drop()
        return value
