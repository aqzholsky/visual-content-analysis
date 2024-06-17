import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateAnalysisResponse(BaseModel):
    request_id: str


class DeleteAnalysisResponse(BaseModel):
    detail: str


class ClassResult(BaseModel):
    class_name: str
    probability: float


class FrameResult(BaseModel):
    frame: str
    classes: List[ClassResult]


class GetAnalysisResponse(BaseModel):
    request_id: uuid.UUID
    timestamp: datetime
    results: List[FrameResult]
