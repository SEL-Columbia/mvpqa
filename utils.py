from config.settings import CUSTOM_REPORTS, FORM_XMLNS


def get_report_id(domain, report):
    """Returns the id of a specified report
    as configured in CUSTOM_REPORTS settings
    """
    rs = CUSTOM_REPORTS.get(domain, None)
    if rs and isinstance(rs, dict):
        return rs.get(report, None)
    return rs


def get_form_xmlns(domain, form):
    """Returns the form xmlns of a specified form
    as configured in FORM_XMLNS settings
    """
    rs = FORM_XMLNS.get(domain, None)
    if rs and isinstance(rs, dict):
        return rs.get(form, None)
    return rs
