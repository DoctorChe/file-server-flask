import os

from pathlib import Path

from flask import jsonify, request, send_from_directory, g
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth, db, create_app
from .utils import get_file_name, get_full_path


app = create_app(os.getenv("CONFIG_TYPE"))


@auth.verify_password
def verify_password(name, password):
    user = User.query.filter_by(name=name).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    files = db.relationship("FileInfo", cascade="all, delete")

    def __init__(self, name):
        self.name = name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class FileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
