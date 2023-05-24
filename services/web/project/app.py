import logging

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from .utils import get_file_name


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s %(message)s")

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


@app.route("/files/", methods=["POST"])
@auth.login_required
def upload():
    if "file" not in request.files:
        logger.warning("Request payload has no file content")
        return jsonify(error="Request payload has no file content"), 400

    file_ = request.files["file"]

    if file_.filename == "":
        logger.warning("Request payload has no file content")
        return jsonify(error="Request payload has no file content"), 400

    file_name = get_file_name(secure_filename(file_.filename))
    full_path = Path("/") / app.config["UPLOAD_FOLDER"] / file_name[:2] / file_name

    if not (parent := full_path.parent).is_dir():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logger.error(f"Permission error while directory creating: {parent} | {e}")
            return jsonify(error="Unable to save file"), 500

    try:
        file_.save(full_path)
    except PermissionError as e:
        logger.error(f"Permission error while file saving: {parent} | {e}")
    except Exception as e:
        logger.error(f"Unknown error while file saving: {full_path} | {e}")
        return jsonify(error="Unable to save file"), 500

    user = User.query.filter_by(name=g.current_user.name).first()
    file_info = FileInfo(name=file_name, user_id=user.id)
    with app.app_context():
        db.session.add(file_info)
        db.session.commit()

    logger.info(f"File saved: {full_path}")
    return jsonify(file_name=full_path.name), 201


@app.route("/files/<string:file_name>", methods=["GET"])
def download(file_name: str):
    directory = Path("/") / app.config["UPLOAD_FOLDER"]
    file_path = f"{file_name[:2]}/{file_name}"
    full_path = directory / file_path

    if full_path.is_file():
        logger.info(f"File is sending: {full_path}")
        return send_from_directory(
            directory=directory, path=file_path, as_attachment=True
        )

    logger.warning(f"File not found: {full_path}")
    return jsonify(error="File not found"), 404


@app.route("/files/<string:file_name>", methods=["DELETE"])
@auth.login_required
def delete(file_name: str):
    full_path = Path("/") / app.config["UPLOAD_FOLDER"] / file_name[:2] / file_name

    file_info = FileInfo.query.filter_by(name=file_name).first()

    if file_info and file_info.user_id != g.current_user.id:
        logger.warning(f"User is not file owner: {g.current_user} | {file_info}")
        return jsonify(error="Unable to delete file"), 403
    else:
        try:
            full_path.unlink(missing_ok=False)
        except FileNotFoundError:
            logger.warning(f"File not found: {full_path}")
            return jsonify(error="File not found"), 404

    with app.app_context():
        db.session.delete(file_info)
        db.session.commit()

    logger.info(f"File deleted: {full_path}")
    return jsonify(result="File deleted"), 204


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
