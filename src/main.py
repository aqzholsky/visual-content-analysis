from fastapi import FastAPI

from src.analysis.router import router as analysis_router
from src.config import DEBUG

app = FastAPI(debug=DEBUG)
app.include_router(analysis_router, prefix="/analysis")
