from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.api.v1.tasks.models import TaskResponse
from backend_workpal.api.v1.tasks.task_router import CurrentUser, Service
from backend_workpal.database.database import get_session
from .models import UserCreate, UserResponse
from .service import UserService
from ..auth.service import get_current_user
from backend_workpal.core.security import get_password_hash

router = APIRouter(
  prefix="/users",
  tags=["users"],
  responses= {404: {"description": "not found"}}
)

user_service = UserService()

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_202_ACCEPTED)
def get_users(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]):

  users = user_service.read_all_users(session)
  return users

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
def get_user_by_id(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
  user_id: int
  ):
  user = user_service.read_user_by_id(user_id, session)

  if not user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"No se encontro usuario con el id {user_id}"
      )
  
  return user

@router.get("/project/{project_id}", response_model=List[TaskResponse], status_code=status.HTTP_202_ACCEPTED)
def get_tasks_by_project(project_id: int, current_user: CurrentUser, service: Service):
  return service.read_tasks_by_project(project_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
  new_user_data: UserCreate,
  session: Annotated[Session, Depends(get_session)],
  ):

  hashed_password = get_password_hash(new_user_data.password)

  created_user = user_service.create_user(new_user_data, hashed_password, session)

  if not created_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No se pudo crear el usuario"
      )

  return created_user

