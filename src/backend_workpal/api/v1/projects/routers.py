from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from ..project_members.models import ProjectMemberResponse, ProjectMemberUpdate
from ..project_join_requests.models import ProjectJoinRequestCreate, ProjectJoinRequestResponse, ProjectJoinRequestUpdate
from ..project_members.models import ProjectMembers
from .models import ProjectCreate, ProjectResponse, ProjectUpdate
from ..project_members.models import ProjectMemberCreate
from .service import ProjectService
from ..project_members.service import ProjectMemberService
from ..project_join_requests.service import JoinRequestService
from ..auth.service import get_current_user, get_current_project_member_user, get_add_member_user

router = APIRouter(
  prefix="/projects",
  tags=["projects"],
  responses= {404: {"description": "not found"}}
)

project_service = ProjectService()

project_member_service = ProjectMemberService()

project_join_request_service = JoinRequestService()


@router.get("/", response_model=List[ProjectResponse], status_code=status.HTTP_202_ACCEPTED)
def get_all_projects(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
):
  projects = project_service.read_all_projects(session)
  return projects

@router.get("/{id_project}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def get_project_by_id(
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

@router.get("/{project_id}/join_requests/", response_model=List[ProjectJoinRequestResponse], status_code=status.HTTP_202_ACCEPTED)
def get_join_requests_by_project_id(
  project_id: int,
  current_member: Annotated[ProjectMembers, Depends(get_add_member_user)],
  session: Annotated[Session, Depends(get_session)],
  ):

  join_requests = project_join_request_service.read_join_request_by_project_id(project_id, session)

  return join_requests

@router.get("/{project_id}/project_members/", response_model=List[ProjectMemberResponse], status_code=status.HTTP_200_OK)
def get_project_members_by_project_id(
  current_user: Annotated[ProjectMemberResponse, Depends(get_current_project_member_user)],
  project_id: int,
  session: Annotated[Session, Depends(get_session)],
  ):

  project_members = project_member_service.get_project_members_by_project_id(project_id, session)

  return project_members

@router.get("/{project_id}/project_member/{member_id}/", response_model=ProjectMemberResponse, status_code=status.HTTP_200_OK)
def get_project_member_by_project_and_member_id(
  current_user: Annotated[ProjectMemberResponse, Depends(get_current_project_member_user)],
  project_id: int,
  member_id: int,
  session: Annotated[Session, Depends(get_session)],
  ):

  project_member = project_member_service.get_project_member_by_project_and_user_ids(project_id, member_id, session)

  if not project_member:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro al usuario con id {member_id} en el proyecto con id {project_id}"
      )

  return project_member

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
def create_project_member(
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

@router.post("/{project_id}/join_request/", response_model=ProjectJoinRequestResponse, status_code=status.HTTP_202_ACCEPTED)
def create_join_request_to_project(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  project_id: int,
  new_join_request_data: ProjectJoinRequestCreate,
  session: Annotated[Session, Depends(get_session)],
):
  new_join_request = project_join_request_service.create_join_request(current_user.id, project_id, new_join_request_data, session)

  if not new_join_request:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"No se pudo crear la solicitud para unirse al proyecto con id {project_id}"
        )

  return new_join_request

@router.put("/{updated_project_id}", response_model=ProjectResponse, status_code=status.HTTP_202_ACCEPTED)
def update_project(
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

@router.put("/{project_id}/join_request/{request_id}", response_model=ProjectJoinRequestResponse, status_code=status.HTTP_202_ACCEPTED)
def update_project_join_request(
  project_id: int,
  request_id: int,
  update_status: ProjectJoinRequestUpdate,
  current_member: Annotated[ProjectMembers, Depends(get_add_member_user)],
  session: Annotated[Session, Depends(get_session)],
):

  updated_join_request = project_join_request_service.update_join_request(request_id, project_id, update_status, session)

  if not updated_join_request:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No fue posible aceptar o cancelar el status"
      )
  
  return updated_join_request

@router.put("/{project_id}/project_member/{member_id}/", response_model= ProjectMemberResponse, status_code=status.HTTP_202_ACCEPTED)
def update_project_member(
  project_id: int,
  member_id: int,
  update_data: ProjectMemberUpdate,
  current_member: Annotated[ProjectMembers, Depends(get_add_member_user)],
  session: Annotated[Session, Depends(get_session)],
  ):

  updatable_member = project_member_service.get_project_member_by_project_and_user_ids(project_id, member_id, session)

  if not updatable_member:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No se encontro el usuario con id {member_id} en el proyecto con id {project_id}")
  
  if updatable_member.is_leader:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No se puede editar al lider del proyecto")

  if updatable_member.id == current_member.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes editar tus propios permisos")

  if not current_member.is_leader:
    if updatable_member.can_invite_members:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el lider puede editar a los usuarios con permisos de invitar usuarios")
    if update_data.can_invite_members:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el lider puede dar permisos de invitar usuarios")

  updated_member = project_member_service.update_project_member(update_data, updatable_member, session)

  if not updated_member:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fue posinle editar al miembro")
  
  return updated_member

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
