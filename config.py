import os

basedir = os.path.abspath(os.path.dirname(__file__))


# smtp.qq.com，使用SSL，端口号465或587
class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or '12632'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <1992592417@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('JADE_DEV_DATABASE_URI')


class DefaultConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('JADE_DEV_DATABASE_URI')


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('JADE_TEST_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'default': DefaultConfig,
    'testing': TestingConfig
}
