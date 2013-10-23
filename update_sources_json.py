import os
import sys
import json

from pybamboo.connection import Connection
from pybamboo.dataset import Dataset


def update_sources(site):
    sources = 'sources.json'
    sources_dir = os.path.join(os.path.dirname(__file__), 'data')
    if isinstance(site, basestring):
        sources = os.path.join(
            os.path.dirname(__file__), 'data',
            site.lower(), 'sources.json')
        sources_dir = os.path.join(sources_dir, site.lower())
    else:
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
            path = os.path.join(sources_dir, k)
            if not os.path.exists(path):
                raise Exception(u"%s does not exist," % path)
            try:
                dataset = Dataset(
                    path=path, connection=connection,
                    na_values=["---", "None"], data_format='csv')
            except Exception, e:
                print u"Exception: Publishing %s failed!\n\t%s" % (k, e)
            else:
                sources_dict['sources'][k] = dataset.id
    f = open(sources, 'w')
    f.write(json.dumps(sources_dict, indent=2))
    f.close()


if __name__ == '__main__':
    arguments = sys.argv[1:]
    site = None
    if len(arguments) >= 1:
        site = arguments[0]
    update_sources(site)
