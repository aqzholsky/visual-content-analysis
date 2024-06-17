import json
import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, File, UploadFile, status
from fastapi.responses import JSONResponse

from .dependencies import FilePathDependency
from .models import CreateAnalysisResponse, DeleteAnalysisResponse, GetAnalysisResponse
from .service import analyze_content
from .utils import construct_upload_file_path

router = APIRouter()


@router.post(
    "/",
    response_model=CreateAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_analysis(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
):
    request_id = str(uuid.uuid4())
    file_location = construct_upload_file_path(file.filename, request_id)

    async with aiofiles.open(file_location, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    background_tasks.add_task(analyze_content, file_location, request_id)

    return {"request_id": request_id}


@router.get("/{request_id}", response_model=GetAnalysisResponse)
async def get_analysis(file_path: FilePathDependency):
    async with aiofiles.open(file_path, "r") as file:
        content = await file.read()
    return JSONResponse(content=json.loads(content))


@router.delete("/{request_id}", response_model=DeleteAnalysisResponse)
async def delete_analysis(file_path: FilePathDependency):
    os.remove(file_path)
    return {"detail": "Analysis deleted"}
