from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend_workpal.database.database import create_db_and_tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)
