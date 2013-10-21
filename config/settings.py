COMMCARE_URL = u'https://www.commcarehq.org'
COMMCARE_USERNAME = u''
COMMCARE_PASSWORD = u''
CUSTOM_REPORTS = {
    'mvp-ruhiira': {
        'pregnancy-visit': '5b465124990a0e7c216b707109eb2cea'
    }
}

try:
    from .local_settings import *
except:
    pass
