import os
import json

from pybamboo.connection import Connection
from pybamboo.dataset import Dataset


def update_sources():
    sources = os.path.join(
        os.path.dirname(__file__), 'sources.json'
    )
    if not os.path.exists(sources):
        raise Exception(u"Please define a sources.json.")
    f = open(sources)
    sources_dict = json.loads(f.read())
    f.close()

    assert 'bamboo_server' in sources_dict
    assert 'sources' in sources_dict

    connection = Connection(sources_dict['bamboo_server'])
    for k, v in sources_dict['sources'].iteritems():
        if v == "":
            path = os.path.join(
                os.path.dirname(__file__), 'data', k
            )
            if not os.path.exists(path):
                raise Exception(u"%s does not exist," % path)
            dataset = Dataset(
                path=path, connection=connection,
                na_values=["---", "None"], data_format='csv')
            sources_dict['sources'][k] = dataset.id
    f = open(sources, 'w')
    f.write(json.dumps(sources_dict, indent=2))
    f.close()


if __name__ == '__main__':
    update_sources()
