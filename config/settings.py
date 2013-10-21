COMMCARE_URL = u'https://www.commcarehq.org'
COMMCARE_USERNAME = u''
COMMCARE_PASSWORD = u''
CUSTOM_REPORTS = {
    'mvp-ruhiira': {
        'pregnancy-visit': '5b465124990a0e7c216b707109eb2cea',
        'household-visit': 'b1817d5823cce017ff35fdfaaf4b2f40',
        'child-visit': '91b622122dcf8f5807f62793dd5c6691'
    }
}

try:
    from .local_settings import *
except:
    pass
