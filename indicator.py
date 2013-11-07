import os
import json

from jinja2 import Environment

from pymongo import MongoClient

from pybamboo.connection import Connection
from pybamboo.dataset import Dataset

from periods import datetimeformat

BAMBOO_URL = "http://localhost:8080"

# load custom dateformat to be used by templates
env = Environment()
env.filters['datetimeformat'] = datetimeformat


class BambooIndicator(object):
    def __init__(self, site=None):
        self.connection = Connection(BAMBOO_URL)
        self._set_sources(site)
        self._db = MongoClient().bamboo_dev

    def _set_sources(self, site=None):
        path = os.path.join(os.path.dirname(__file__), 'sources.json')
        if isinstance(site, basestring):
            path = os.path.join(
                os.path.dirname(__file__), 'data',
                site.lower(), 'sources.json'
            )
        f = open(path)
        self._sources_dict = json.loads(f.read())
        self._sources = self._sources_dict['sources']
        self.connection = Connection(self._sources_dict['bamboo_server'])

    def _calculation_exists(self, name, dataset):
        calculations = dataset.get_calculations()
        if 'error' in calculations:
            raise Exception(calculations['error'])
        for calc in calculations:
            if isinstance(calc, dict) and calc['name'] == name:
                return True
        return False

    def get_indicator_value(self, indicator, period):
        assert 'value' in indicator
        assert isinstance(indicator, dict)
        value = indicator['value']
        result = result_num = result_den = None
        if 'sum' in value:
            result = self._get_sum('sum', value, period)
        if 'aggregations' in value:
            result = self._get_aggregate('aggregations', value, period)

        if 'proportion' in value:
            proportion = value['proportion']
            denominator = numerator = None
            if 'denominator' in proportion:
                denominator = self._get_sum('denominator', proportion, period)
            if 'numerator' in proportion:
                numerator = self._get_sum('numerator', proportion, period)
            if denominator == 0:
                result = 0
            else:
                result = round(
                    100 * (float(numerator) / float(denominator)), 2)
            result_num = numerator
            result_den = denominator

        if 'python' in value:
            params = value['python']
            definitionClass = self._get_definition(params['name'])
            dataset_id = params['dataset_id']
            # dataset_id form sources.json is most recent
            if dataset_id != self._sources[params['source']]\
                    and self._sources[params['source']] != "":
                dataset_id = self._sources[params['source']]
            defInstance = definitionClass(self._db, dataset_id)
            rs = defInstance.get_value(period)
            if isinstance(rs, tuple):
                result, result_num, result_den = rs
            else:
                result = rs
        return result, result_num, result_den

    def _get_definition(self, name):
            m = __import__(
                ''.join(['pydefinitions.', name]),
                globals(), locals(), ['Definition'], -1)
            return m.Definition

    def _add_calculation(self, calculation, dataset, period):
        name = env.from_string(calculation['name'])\
            .render(period=period)
        formula = env.from_string(calculation['formula'])\
            .render(period=period)
        calc_exists = self._calculation_exists(
            name, dataset)
        if not calc_exists:
            calc = dataset.add_calculation(
                name=name, formula=formula)
            if not calc:
                raise Exception(
                    u"Failed to add calculation %s: %s" % (name, formula))

    def _get_sum(self, key, value, period):
        sum_value = 0
        for v in value[key]:
            if 'aggregations' in v:
                sum_value += self._get_aggregate('aggregations', v, period)
                continue
            dataset_id = v['dataset_id']
            # dataset_id form sources.json is most recent
            if dataset_id != self._sources[v['source']]\
                    and self._sources[v['source']] != "":
                dataset_id = self._sources[v['source']]
            dataset = Dataset(
                dataset_id=dataset_id, connection=self.connection)

            params = {}
            if 'calculation' in v:
                # check or create calculations
                if isinstance(v['calculation'], list):
                    for calculation in v['calculation']:
                        self._add_calculation(calculation, dataset, period)
                if isinstance(v['calculation'], dict):
                    self._add_calculation(v['calculation'], dataset, period)
            if 'query' in v:
                query_string = json.dumps(v['query'])
                template = env.from_string(query_string)
                query_string = template.render(period=period)
                v['query'] = json.loads(query_string)
                params['query'] = v['query']
            if 'count' in v and 'query' in v:
                params['count'] = v['count']
            if 'distinct' in v:
                params['distinct'] = v['distinct']
            val = dataset.get_data(**params)
            if isinstance(val, dict):
                raise Exception("Bamboo Error: %s" % val)
            sum_value += val
        return sum_value

    def _get_aggregate(self, key, value, period):
        sum_value = 0
        for v in value[key]:
            dataset_id = v['dataset_id']
            # dataset_id form sources.json is most recent
            if dataset_id != self._sources[v['source']]\
                    and self._sources[v['source']] != "":
                dataset_id = self._sources[v['source']]
            dataset = Dataset(
                dataset_id=dataset_id, connection=self.connection)

            params = {}
            if 'calculation' in v:
                # check or create calculations
                if isinstance(v['calculation'], list):
                    for calculation in v['calculation']:
                        self._add_calculation(calculation, dataset, period)
                if isinstance(v['calculation'], dict):
                    self._add_calculation(v['calculation'], dataset, period)
            if 'query' in v:
                query_string = json.dumps(v['query'])
                template = env.from_string(query_string)
                query_string = template.render(period=period)
                v['query'] = json.loads(query_string)
                params['query'] = v['query']
            # if 'count' in v and 'query' in v:
            #     params['count'] = v['count']
            if 'distinct' in v:
                params['distinct'] = v['distinct']
            data = dataset.get_data(format='csv', **params)
            if data.strip() == '':
                # no data to create a dataset - skip
                continue
            # create a aggregate dataset
            aggr_dataset = Dataset(
                content=data,
                data_format='csv',
                connection=self.connection)
            if 'aggregate' in v:
                # check or create calculations
                if isinstance(v['aggregate'], list):
                    for calculation in v['aggregate']:
                        calc = aggr_dataset.add_calculation(
                            name=calculation['name'],
                            formula=calculation['formula']
                        )
                        if calc:
                            aggr_ds = aggr_dataset.get_aggregations()['']
                            k = aggr_ds.get_data()
                            val = k[0][calculation['name']]
                            if isinstance(val, basestring):
                                raise ValueError("Dataset %s return %s"
                                                 % (aggr_ds.id, val))
                            sum_value += val
                            aggr_ds.delete()
                if isinstance(v['aggregate'], dict):
                    calculation = v['aggregate']
                    calc = aggr_dataset.add_calculation(
                        name=calculation['name'],
                        formula=calculation['formula']
                    )
                    if calc:
                        aggr_ds = aggr_dataset.get_aggregations()['']
                        k = aggr_ds.get_data()
                        val = k[0][calculation['name']]
                        if isinstance(val, basestring):
                            raise ValueError("Dataset %s return %s"
                                             % (aggr_ds.id, val))
                        sum_value += val
                        aggr_ds.delete()
            aggr_dataset.delete()
        return sum_value
