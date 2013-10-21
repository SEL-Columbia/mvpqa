COMMCARE_URL = u'https://www.commcarehq.org'
COMMCARE_USERNAME = u''
COMMCARE_PASSWORD = u''

try:
    from .local_settings import *
except:
    pass
