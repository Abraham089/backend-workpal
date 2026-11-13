from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from .models import RolesResponse
from .service import RoleService
from ..auth.service import get_current_user

router = APIRouter(
  prefix="/roles",
  tags=["roles"],
  responses= {404: {"description": "not found"}}
)

role_service = RoleService()

@router.get("/", response_model=List[RolesResponse], status_code=status.HTTP_202_ACCEPTED)
def get_all_roles(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]
  ):

  roles = role_service.read_all_roles(session)
  return roles

@router.get("/{role_id}", response_model=RolesResponse, status_code=status.HTTP_202_ACCEPTED)
def get_role_by_id(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
  role_id: int
  ):
  role = role_service.read_role_by_id(role_id, session)

  if not role:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"No se encontro el rol con el id {role_id}"
      )
  
  return role
