class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "dasod234234fsda"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    CLIENT_IMAGES = r"C:\Users\Computador\Documents\learning-flask\app\static\client\img"
    CLIENT_CSV = r"C:\Users\Computador\Documents\learning-flask\app\static\client\csv"
    CLIENT_REPORTS = r"C:\Users\Computador\Documents\learning-flask\app\static\client\reports"

    UPLOADS = "/home/username/app/app/static/images/uploads"
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True
