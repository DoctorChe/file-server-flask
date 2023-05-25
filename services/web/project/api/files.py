import os

from pathlib import Path

from flask import jsonify, send_from_directory, request, g

from project import logger, auth, db
from project.api import api
from project.models import FileInfo, User
from project.utils import get_full_path, get_file_name


UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
MESSAGE_NO_FILE_CONTENT = "Request payload has no file content"


@api.route("/files/", methods=["POST"])
@auth.login_required
def upload():
    if "file" not in request.files:
        logger.warning(MESSAGE_NO_FILE_CONTENT)
        return jsonify(error=MESSAGE_NO_FILE_CONTENT), 400

    file_ = request.files["file"]

    if file_.filename == "":
        logger.warning(MESSAGE_NO_FILE_CONTENT)
        return jsonify(error=MESSAGE_NO_FILE_CONTENT), 400

    file_bytes = file_.stream.read()
    file_name = get_file_name(file_bytes)

    file_info = FileInfo.query.filter_by(name=file_name).first()
    if file_info is not None:
        logger.warning(
            f"Attempt to upload an existing file: filename={file_name} username={g.current_user.name}"
        )
        return jsonify(error="Unable to upload file. File already exist on server"), 403

    full_path = get_full_path(UPLOAD_FOLDER, file_name)

    if not (parent := full_path.parent).is_dir():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logger.error(f"Permission error while directory creating: {parent} | {e}")
            return jsonify(error="Unable to save file"), 500

    try:
        with open(full_path, 'wb') as f:
            f.write(file_bytes)
    except PermissionError as e:
        logger.error(f"Permission error while file saving: {parent} | {e}")
    except Exception as e:
        logger.error(f"Unknown error while file saving: {full_path} | {e}")
        return jsonify(error="Unable to save file"), 500

    user = User.query.filter_by(name=g.current_user.name).first()
    file_info = FileInfo(name=file_name, user_id=user.id)
    db.session.add(file_info)
    db.session.commit()

    logger.info(f"File saved: {full_path}")
    return jsonify(file_name=full_path.name), 201


@api.route("/files/<string:file_name>", methods=["DELETE"])
@auth.login_required
def delete(file_name: str):
    full_path = get_full_path(UPLOAD_FOLDER, file_name)

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

    file_info = db.session.merge(file_info)
    db.session.delete(file_info)
    db.session.commit()

    logger.info(f"File deleted: {full_path}")
    return jsonify(result="File deleted"), 204


@api.route("/files/<string:file_name>", methods=["GET"])
def download(file_name: str):
    directory = Path("/") / UPLOAD_FOLDER
    file_path = f"{file_name[:2]}/{file_name}"
    full_path = get_full_path(UPLOAD_FOLDER, file_name)

    if full_path.is_file():
        logger.info(f"File is sending: {full_path}")
        return send_from_directory(
            directory=directory, path=file_path, as_attachment=True
        )

    logger.warning(f"File not found: {full_path}")
    return jsonify(error="File not found"), 404
