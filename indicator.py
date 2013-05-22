import os
import json

from pybamboo.connection import Connection
from pybamboo.dataset import Dataset

BAMBOO_URL = "http://localhost:8080"


class BambooIndicator(object):
    def __init__(self):
        self.connection = Connection(BAMBOO_URL)
        self._set_sources()

    def _set_sources(self):
        path = os.path.join(
            os.path.dirname(__file__), 'sources.json'
        )
        f = open(path)
        self._sources_dict = json.loads(f.read())
        self._sources = self._sources_dict['sources']

    def _calculation_exists(self, name, dataset):
        for calc in dataset.get_calculations():
            if calc['name'] == name:
                return True
        return False

    def get_indicator_value(self, indicator, period):
        assert 'value' in indicator
        assert isinstance(indicator, dict)
        value = indicator['value']
        if 'sum' in value:
            sum_value = 0
            for v in value['sum']:
                dataset_id = v['dataset_id']
                # dataset_id form sources.json is most recent
                if dataset_id != self._sources[v['source']]:
                    dataset_id = self._sources[v['source']]
                dataset = Dataset(
                    dataset_id=dataset_id, connection=self.connection)
                print dataset
                if 'calculation' in v:
                    # check or create calculations
                    if isinstance(v['calculation'], list):
                        for calculation in v['calculation']:
                            calc_exists = self._calculation_exists(
                                calculation.name, dataset)
                            if not calc_exists:
                                dataset.add_calculation(json=calculation)
                    if isinstance(v['calculation'], dict):
                        if not self._calculation_exists(
                                v['calculation']['name'], dataset):
                            dataset.add_calculation(json=v['calculation'])
                if 'query' in v:
                    query_string = json.dumps(v['query'])
                    query_string = query_string.replace(
                        '{{period_start}}', period.start.strftime("%Y-%m-%d"))
                    query_string = query_string.replace(
                        '{{period_end}}', period.end.strftime("%Y-%m-%d"))
                    v['query'] = json.loads(query_string)
                if 'count' in v and 'query' in v:
                    sum_value += dataset.get_data(
                        query=v['query'], count=v['count'])
            return sum_value
