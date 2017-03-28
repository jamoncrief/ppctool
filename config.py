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

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# administrator list
ADMINS = ['james.adam.moncrief@gmail.com']
