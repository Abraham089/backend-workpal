from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from .models import ProjectCreate, ProjectResponse, ProjectUpdate
from .service import ProjectService
from ..auth.service import get_current_user

router = APIRouter(
  prefix="/projects",
  tags=["projects"],
  responses= {404: {"description": "not found"}}
)

project_service = ProjectService()


@router.get("/", response_model=List[ProjectResponse], status_code=status.HTTP_202_ACCEPTED)
def get_all_projects(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
):
  projects = project_service.read_all_projects(session)
  return projects

@router.get("/{id_project}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def get_projects_by_id(
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

  created_project = project_service.create_project(new_project_data,current_user.id, session)
  

  if not created_project:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No se pudo crear el proyecto"
      )

  return created_project

@router.put("/{updated_project_id}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def put_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  updated_project_id: int,
  updated_project: ProjectUpdate,
  session: Annotated[Session, Depends(get_session)],
  ):
  
  project_updated = project_service.read_project_by_id(updated_project_id, session)

  if not project_updated:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro proyecto con id {updated_project_id} para editar"
      )
    
  if not project_service.user_can_edit(project_updated,current_user.id, session):
    raise HTTPException(
      status_code=404,
      detail="No tiene permisos para modificar el projecto"
    )
    
  project = project_service.update_project(updated_project_id, updated_project, session)

  return project

@router.delete("/{delete_project_id}", status_code=status.HTTP_200_OK)
def delete_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  delete_project_id: int,
  session: Annotated[Session, Depends(get_session)],
):

  deleted_project = project_service.read_project_by_id(delete_project_id, session)

  if not deleted_project:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro proyecto con id {delete_project_id}"
      )
    
  if not project_service.user_can_edit(deleted_project, current_user.id, session):
    raise HTTPException(
      status_code=403,
      detail="No tienes permiso para eliminar este proyecto"
      )
    
  project = project_service.delete_project(delete_project_id, session)
  
  return project
