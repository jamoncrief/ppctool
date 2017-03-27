WTF_CSRF_ENABLED = True
SECRET_KEY = 'monchief'

GOOGLE_LOGIN_CLIENT_ID = "603499396792-bl8scdsmlncnjiff8l61f0e8l6li3din.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "t2hCcF5NCR5Iq3sewc1T67aQ"

OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}


import os
basedir = os.path.abspath(os.path.dirname(__file__))
