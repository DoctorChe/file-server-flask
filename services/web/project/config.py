import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    USER_LOGIN = os.getenv("USER_LOGIN")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
