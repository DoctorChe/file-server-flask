from werkzeug.security import generate_password_hash, check_password_hash

from project import db


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
