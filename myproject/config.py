import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '8e0acd6b4257c1f854e6f5ca872d3019'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_DEBUG = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'babatundeadeniyi25@gmail.com'
    MAIL_PASSWORD = 'emmana!234'
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX')
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POST_PER_PAGE = 8
    FLASKY_FOLLOWERS_PER_PAGE = 4
    FLASKY_COMMENTS_PER_PAGE = 5
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config): 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        import logging
        from logging.handlers import SMTPHandler
        credential = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error ',
                credentials=credentials,
                secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}



