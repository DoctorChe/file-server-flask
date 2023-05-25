import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    USER_LOGIN = os.getenv("USER_LOGIN")
    USER_PASSWORD = os.getenv("USER_PASSWORD")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
