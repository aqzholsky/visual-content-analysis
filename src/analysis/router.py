import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, File, UploadFile, status
from fastapi.responses import JSONResponse

from .crud import delete_analysis_result, get_analysis_by_request_id, is_analysis_exists
from .dependencies import DatabaseDependency
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
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    request_id = str(uuid.uuid4())
    file_location = construct_upload_file_path(file.filename, request_id)

    async with aiofiles.open(file_location, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    background_tasks.add_task(analyze_content, file_location, request_id)

    return {"request_id": request_id}


@router.get(
    "/{request_id}",
    response_model=GetAnalysisResponse,
)
async def get_analysis(request_id: str, db: DatabaseDependency):
    if content := await get_analysis_by_request_id(db, request_id):
        return JSONResponse(content=content)
    return JSONResponse(
        content={"detail": "Analysis not found"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete(
    "/{request_id}",
    response_model=DeleteAnalysisResponse,
)
async def delete_analysis(request_id: str, db: DatabaseDependency):
    if not await is_analysis_exists(db, request_id):
        return JSONResponse(
            content={"detail": "Analysis not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    await delete_analysis_result(db, request_id)
    return {"detail": "Analysis deleted"}
