import json
from pymongo import MongoClient

from bamboo.models.dataset import Dataset
from bamboo.models.observation import Observation
from bamboo.core.frame import DATASET_ID

from bson.code import Code
from jinja2 import Template

from periods import Period

db = MongoClient().bamboo_dev

mapper_str = """
function(){
    value = this;
    key = this['{{case__case_id}}'];
    if(isNaN(value["{{num_using_fp}}"])){
        value["{{num_using_fp}}"] = 0;
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
    if(isNaN(reducedValue["{{num_using_fp}}"])){
        reducedValue["{{num_using_fp}}"] = 0;
    }
    return reducedValue;
}
"""

query_str = """
{"{{dataset_id_field}}": "{{dataset.dataset_id}}",
"{{meta_timeend}}": {
              "$gte": "{{period.start}}", 
              "$lte": "{{period.end}}"
            }
}
"""
aggregate_str = """
{"$group": {"_id": 0, "total": {"$sum": "$value.{{num_using_fp}}"}}}
"""
dataset_id = "5791793ac29b4d77b20cf1a04d8e7161"
dataset = Dataset.find_one(dataset_id)
period = Period.month_period(2013, 3)

if dataset:
    fields = Observation.encoding(dataset)
    fields["dataset"] = dataset
    fields['dataset_id_field'] = fields[DATASET_ID]
    fields['period'] = Period.month_period(2013, 3)
    mapper = Code(Template(mapper_str).render(fields))
    reducer = Code(Template(reducer_str).render(fields))
    query = json.loads(Template(query_str).render(fields))
    aggregate = json.loads(Template(aggregate_str).render(fields))
    results = db.observations.map_reduce(mapper, reducer, 'myresults_fp', query=query)
    if results.count():
        value = results.aggregate(aggregate)
        print  value['result'][0]['total']
        assert value['result'][0]['total'] == 3141
    else:
        import ipdb; ipdb.set_trace()
    db.myresults_fp.drop()
