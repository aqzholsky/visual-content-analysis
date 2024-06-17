import os

from .constants import RESULT_FILE_DIR, UPLOAD_FILE_DIR


def construct_upload_file_path(file_name: str, uuid: str) -> str:
    os.makedirs(UPLOAD_FILE_DIR, exist_ok=True)

    return f"{UPLOAD_FILE_DIR}/{uuid}_{file_name}"


def construct_result_file_path(request_id):
    os.makedirs(RESULT_FILE_DIR, exist_ok=True)

    return f"{RESULT_FILE_DIR}/result_{request_id}.json"
