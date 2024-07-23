import os

from .constants import UPLOAD_FILE_DIR


def construct_upload_file_path(file_name: str, uuid: str) -> str:
    os.makedirs(UPLOAD_FILE_DIR, exist_ok=True)

    return f"{UPLOAD_FILE_DIR}/{uuid}_{file_name}"
