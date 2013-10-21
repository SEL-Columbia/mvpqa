import os
import sys
import requests

from requests.auth import HTTPDigestAuth
from tempfile import NamedTemporaryFile
from urlparse import urljoin
from zipfile import ZipFile

from config.settings import COMMCARE_URL, COMMCARE_USERNAME, COMMCARE_PASSWORD

AUTH = HTTPDigestAuth(COMMCARE_USERNAME, COMMCARE_PASSWORD)


def download_from_commcare(url_path):
    """Given a url path, downloads an export from commcare"""
    url = urljoin(COMMCARE_URL, url_path)
    req = requests.get(url, auth=AUTH)
    if req.status_code != 200:
        raise Exception(u"Commcare responded: %s with status code %s" %
                        (req.content, req.status_code))
    f = NamedTemporaryFile()
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
            f.flush()
    return f


def download_cases(domain):
    """Downloads cases,referral,user csv zip file form commcare.
    The extracted Case.csv is placed in data/DOMAIN/latest/case_export_all.csv
    """
    case_path = '/a/%(domain)s/reports/download/cases/?format=csv' % {
        'domain': domain}
    f = download_from_commcare(case_path)
    z = ZipFile(f, 'r')
    zdst = os.path.join('data', domain, 'latest')
    src = os.path.join(zdst, 'Case.csv')
    dst = os.path.join(zdst, 'case_export_all.csv')
    if 'Case.csv' in z.NameToInfo:
        z.extract(z.NameToInfo['Case.csv'], zdst)
        if os.path.exists(src):
            os.rename(src, dst)
            print u"Successfully downloaded case_export_all.csv"


if __name__ == '__main__':
    arguments = sys.argv[1:]
    domain = what = None
    if len(arguments) >= 1:
        domain = arguments[0]
    if len(arguments) >= 2:
        what = arguments[1]
    if not domain:
        print (u"domain arguement is expected! e.g\n$"
               u" python pull_data.py mvp-ruhiira ...")
        exit(0)
    if what == 'cases' or what == 'case':
        download_cases(domain)
    else:
        print (u"Missing or Incorrect action specified!"
               u" Expected cases, pregnancy, ...\ni.e\n$"
               u"python pull_data.py mvp-ruhiira cases")
