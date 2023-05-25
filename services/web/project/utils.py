import hashlib

from pathlib import Path


def get_file_name(file: bytes) -> str:
    return hashlib.md5(file).hexdigest()


def get_full_path(upload_folder: str, file_name: str) -> Path:
    return Path("/") / upload_folder / file_name[:2] / file_name
