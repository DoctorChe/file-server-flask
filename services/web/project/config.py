import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SECRET_KEY = os.getenv("SECRET_KEY")
