import logging

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from .utils import get_file_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s %(message)s")

app = Flask(__name__)
app.config.from_object("project.config.Config")


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/files/", methods=["POST"])
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
def delete(file_name: str):
    full_path = Path("/") / app.config["UPLOAD_FOLDER"] / file_name[:2] / file_name

    try:
        full_path.unlink(missing_ok=False)
    except FileNotFoundError:
        logger.warning(f"File not found: {full_path}")
        return jsonify(error="File not found"), 404

    logger.info(f"File deleted: {full_path}")
    return jsonify(result="File deleted"), 204
