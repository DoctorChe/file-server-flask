import hashlib


def get_file_name(file):
    return hashlib.md5(file.encode()).hexdigest()
