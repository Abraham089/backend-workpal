from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from .models import ProjectCreate, ProjectResponse
from .service import ProjectService
from ..auth.service import get_current_user

router = APIRouter(
  prefix="/projects",
  tags=["projects"],
  responses= {404: {"description": "not found"}}
)

project_service = ProjectService()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  new_project_data: ProjectCreate,
  session: Annotated[Session, Depends(get_session)],
  ):

  created_project = project_service.create_project(new_project_data, session)

  if not created_project:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No se pudo crear el proyecto"
      )

  return created_project