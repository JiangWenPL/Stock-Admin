import os

basedir = os.path.abspath ( os.path.dirname ( __file__ ) )

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join ( basedir, 'app.db' )
SQLALCHEMY_BINDS = {
    # 'stock':        'mysql://root:root@localhost/stock'
    'stock': 'mysql://root:123456@localhost:3306/stock'
}
SQLALCHEMY_MIGRATE_REPO = os.path.join ( basedir, 'db_repository' )
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY = '123456'

# class Config ( object ):
# Send confine to center trading system every 8:00 AM on weekday
JOBS = [
    {
        'id': 'send_confine_to_center',
        'func': 'app.models:send_confine_to_center',
        'args': (),
        'trigger': {
            'type': 'cron',
            'day_of_week': "mon-fri",
            # 'hour': '8',
            # 'minute': '0',
            'hour': '0-23',
            'minute': '0-59',
            'second': '*/10'
        },
    }
]

SCHEDULER_API_ENABLED = True
