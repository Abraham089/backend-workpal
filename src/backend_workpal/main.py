from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from backend_workpal.core.config import settings
from backend_workpal.api.v1.api import api_router

origins = [
    settings.FRONTEND_URL,
    settings.FRONTEND_IP_URL
]

from backend_workpal.database.database import create_db_and_tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)