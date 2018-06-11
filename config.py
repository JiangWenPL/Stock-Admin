import os

basedir = os.path.abspath ( os.path.dirname ( __file__ ) )

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join ( basedir, 'app.db' )
SQLALCHEMY_BINDS = {
    'record':        'mysql://root:root@localhost/record'
}
SQLALCHEMY_MIGRATE_REPO = os.path.join ( basedir, 'db_repository' )
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY = '123456'
