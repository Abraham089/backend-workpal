from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.backend_workpal.database.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)
