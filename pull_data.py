import os
import sys
import requests

from requests.auth import HTTPDigestAuth
from tempfile import NamedTemporaryFile
from urlparse import urljoin
from zipfile import ZipFile

from config.settings import COMMCARE_URL, COMMCARE_USERNAME, COMMCARE_PASSWORD
from utils import get_form_xmlns

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


def download_custom_reports(domain, report_id, report_name):
    """Downloads custom report data csv zip export from commcare.
    The extracted csv is placed in data/DOMAIN/latest/Pregnancy Visit.csv.
    :domain - commcare domain
    :report_id - custom report id for report
    """
    if not report_id:
        raise Exception(u"Please ensure the custom report id"
                        u" is configured in CUSTOM_REPORTS settings.")
    url_path = "/a/%(domain)s/reports/export/custom/%(id)s/download/"\
        "?format=csv" % {'domain': domain, 'id': report_id}
    f = download_from_commcare(url_path)
    z = ZipFile(f, 'r')
    zdst = os.path.join('data', domain, 'latest')
    dst = os.path.join(zdst, report_name)
    if z.NameToInfo.keys():
        filename = z.NameToInfo.keys()[0]
        src = os.path.join(zdst, filename)
        z.extract(z.NameToInfo[filename], zdst)
        if os.path.exists(src):
            os.rename(src, dst)
            print u"Successfully downloaded %s" % report_name


def download_form_data(domain, form_xmlns, report_name):
    if not form_xmlns:
        raise Exception(u"Please ensure the form xlmns "
                        u"is configured in FORMS_XLMNS in settings.")
    url_path = ("/a/%(domain)s/reports/export/"
                "?export_tag=%%22%(form_xmlns)s%%22"
                "&format=csv" % {'domain': domain, 'form_xmlns': form_xmlns})
    f = download_from_commcare(url_path)
    z = ZipFile(f, 'r')
    zdst = os.path.join('data', domain, 'latest')
    dst = os.path.join(zdst, report_name)
    filename = '#.csv'
    if '#.csv' in z.NameToInfo:
        src = os.path.join(zdst, filename)
        z.extract(z.NameToInfo[filename], zdst)
        if os.path.exists(src):
            os.rename(src, dst)
            print u"Successfully downloaded %s" % report_name


def download_pregancy_visits(domain, report='pregnancy-visit',
                             name='Pregnancy Visit.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)
    # report_id = get_report_id(domain, report)
    # download_custom_reports(domain, report_id, name)


def download_child_list_visit(domain, report='child-visit',
                              name='Child List Visit.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)
    # report_id = get_report_id(domain, report)
    # download_custom_reports(domain, report_id, name)


def download_child_close(domain, report='child-close',
                         name='Child List Close.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)


def download_pregnancy_outcome(domain, report='pregnancy-outcome',
                               name='Pregnancy Outcome.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)


def download_death_without_registration(domain, report='death',
                                        name='Death without Registration.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)


def download_household_visit(domain, report='household-visit',
                             name='Household Visit.csv'):
    form_xmlns = get_form_xmlns(domain, report)
    download_form_data(domain, form_xmlns, name)
    # report_id = get_report_id(domain, report)
    # download_custom_reports(domain, report_id, name)


HELP_MSG = (u"Missing or Incorrect action specified!"
            u" Expected cases, pregnancy-visit, ...\ni.e"
            u"\n$ python pull_data.py %(domain)s all"
            u"\n$ python pull_data.py %(domain)s cases"
            u"\n$ python pull_data.py %(domain)s child-visit"
            u"\n$ python pull_data.py %(domain)s child-close"
            u"\n$ python pull_data.py %(domain)s death"
            u"\n$ python pull_data.py %(domain)s household visit"
            u"\n$ python pull_data.py %(domain)s pregnancy-visit"
            u"\n$ python pull_data.py %(domain)s pregnancy-outcome")


if __name__ == '__main__':
    arguments = sys.argv[1:]
    domain = report = None
    if len(arguments) >= 1:
        domain = arguments[0]
    if len(arguments) >= 2:
        report = arguments[1]
    if not domain:
        print (u"domain arguement is expected! e.g\n %s" %
               (HELP_MSG % {'domain': 'replace_with_commcare_domain'}))
        exit(0)
    if report == 'cases' or report == 'case':
        download_cases(domain)
    elif report == 'child-visit':
        download_child_list_visit(domain)
    elif report == 'child-close':
        download_child_close(domain)
    elif report == 'death':
        download_death_without_registration(domain)
    elif report == 'household-visit':
        download_household_visit(domain)
    elif report == 'pregnancy-visit':
        download_pregancy_visits(domain)
    elif report == 'pregnancy-outcome':
        download_pregnancy_outcome(domain)
    elif report == 'all':
        download_cases(domain)
        download_pregancy_visits(domain)
        download_pregnancy_outcome(domain)
        download_death_without_registration(domain)
        download_household_visit(domain)
        download_child_list_visit(domain)
        download_child_close(domain)
    else:
        print HELP_MSG % domain
