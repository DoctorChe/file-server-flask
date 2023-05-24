import hashlib

from pathlib import Path


def get_file_name(file):
    return hashlib.md5(file.encode()).hexdigest()


def get_full_path(upload_folder, file_name):
    return Path("/") / upload_folder / file_name[:2] / file_name
