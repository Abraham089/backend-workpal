from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from ..project_members.models import ProjectMemberResponse
from .models import ProjectCreate, ProjectResponse, ProjectUpdate
from ..project_members.models import ProjectMemberCreate
from .service import ProjectService
from ..project_members.service import ProjectMemberService
from ..auth.service import get_current_user, get_current_project_member_user

router = APIRouter(
  prefix="/projects",
  tags=["projects"],
  responses= {404: {"description": "not found"}}
)

project_service = ProjectService()

project_member_service = ProjectMemberService()


@router.get("/", response_model=List[ProjectResponse], status_code=status.HTTP_202_ACCEPTED)
def get_all_projects(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
):
  projects = project_service.read_all_projects(session)
  return projects

@router.get("/{id_project}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def get_all_projects(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  id_project: int,
  session: Annotated[Session, Depends(get_session)],
):
  project = project_service.read_project_by_id(id_project, session)

  if not project:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro proyecto con el id {id_project}"
      )
  return project

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

@router.post("/{project_id}/members/", response_model=bool, status_code=status.HTTP_201_CREATED)
def add_project_member(
  current_user: Annotated[ProjectMemberResponse, Depends(get_current_project_member_user)],
  project_id: int,
  new_member_data: ProjectMemberCreate,
  session: Annotated[Session, Depends(get_session)],
  ):

  if current_user.can_invite_members is False:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="No se tiene permiso para añadir miembros"
      )
  
  new_member = project_member_service.create_project_member(project_id, new_member_data, session)

  if not new_member:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"No se pudo agregar el usuario con id {new_member_data.user_id} al proyecto con id {project_id}"
      )

  return True

@router.put("/{updated_project_id}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def put_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  updated_project_id: int,
  updated_project: ProjectUpdate,
  session: Annotated[Session, Depends(get_session)],
  ):
  
  project_updated = project_service.update_project(updated_project_id, updated_project, session)

  if not project_updated:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro proyecto con id {updated_project_id} para editar"
      )

  return project_updated

@router.delete("/{delete_project_id}", status_code=status.HTTP_200_OK)
def delete_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  delete_project_id: int,
  session: Annotated[Session, Depends(get_session)],
):

  deleted_project = project_service.delete_project(delete_project_id, session)

  if not deleted_project:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro proyecto con id {delete_project_id}"
      )
  
  return deleted_project
