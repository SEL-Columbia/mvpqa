from config.settings import CUSTOM_REPORTS


def get_report_id(domain, report):
    """Returns the id of a specified report
    as configured in CUSTOM_REPORTS settings
    """
    rs = CUSTOM_REPORTS.get(domain, None)
    if rs and isinstance(rs, dict):
        return rs.get(report, None)
    return rs
