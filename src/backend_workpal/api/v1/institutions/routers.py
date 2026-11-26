from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from .models import InstitutionResponse, InstitutionCreate
from ..users.models import UserResponse
from .service import InstitutionService
from ..auth.service import get_admin_user
from backend_workpal.database.database import get_session

router = APIRouter(
  prefix="/institutions",
  tags=["institutions"],
  responses= {404: {"description": "not found"}}
)

institution_service = InstitutionService()

@router.get("/", response_model=List[InstitutionResponse], status_code=status.HTTP_200_OK)
def read_institutions(
  current_user: Annotated[UserResponse, Depends(get_admin_user)],
  session: Annotated[Session, Depends(get_session)],
):
  
  institutions = institution_service.get_all_institutions(session)

  return institutions

@router.get("/{institution_id}", response_model=InstitutionResponse, status_code=status.HTTP_200_OK)
def read_institution_by_id(
  current_user: Annotated[UserResponse, Depends(get_admin_user)],
  institution_id: int,
  session: Annotated[Session, Depends(get_session)],
):
  
  institution = institution_service.get_institution_by_id(institution_id, session)

  if not institution:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No se encontro la institucion con id {institution_id}"
      )
  
  return institution

@router.post("/", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
def post_new_institution(
  current_user: Annotated[UserResponse, Depends(get_admin_user)],
  institution_data: InstitutionCreate,
  session: Annotated[Session, Depends(get_session)],
):
  new_institution = institution_service.create_institution(institution_data, session)

  if not new_institution:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No fue posible crear la institucion"
      )
  
  return new_institution