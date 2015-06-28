import os
class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = "secret"
    THREADS_PER_PAGE = 2
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    DATABASE_CONNECT_OPTIONS = {}

