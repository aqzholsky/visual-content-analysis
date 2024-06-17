import os
from typing import Annotated

from fastapi import Depends, HTTPException

from .utils import construct_result_file_path


def file_path_dependency(request_id: str = "") -> str:
    file_path = construct_result_file_path(request_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Analysis not found")

    return file_path


FilePathDependency = Annotated[str, Depends(file_path_dependency)]
