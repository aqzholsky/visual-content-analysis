from fastapi import FastAPI

from src.analysis.router import router as analysis_router
from src.config import DEBUG
from src.db.mongodb_utils import close_mongo_connection, connect_to_mongo

app = FastAPI(debug=DEBUG)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(analysis_router, prefix="/analysis")
