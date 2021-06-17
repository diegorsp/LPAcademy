class Config(object):
    pass

class ProConfig(object):
    pass

class DevConfig(object):
    
    SENDGRID_API_KEY='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'
    DEFAULT_SENDER = 'diegorspassos@gmail.com'
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY= 'hard to guess string'
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT ='587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = SENDGRID_API_KEY
    MAIL_DEFAULT_SENDER = DEFAULT_SENDER

    