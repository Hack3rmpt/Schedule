import os

class Config(object):
    USER = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', '1532')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5435)
    DB = os.environ.get('POSTGRES_DB', 'Testdb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = '09182b3cr9b8721sk901j238ys19208nxy9'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    LOGGING_CONFIG = {
        'version': 1,
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'level': 'DEBUG'
            }
        },
        'root': {
            'handlers': ['file'],
            'level': 'DEBUG'
        }
    }


