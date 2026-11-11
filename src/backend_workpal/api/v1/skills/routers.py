from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from .models import SkillCreate, SkillResponse
from .service import SkillService
from ..auth.service import get_current_user

router = APIRouter(
  prefix="/skills",
  tags=["skills"],
  responses= {404: {"description": "not found"}}
)

skill_service = SkillService()

@router.get("/", response_model=List[SkillResponse], status_code=status.HTTP_202_ACCEPTED)
def get_skills(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]
  ):

  skills = skill_service.read_all_skills(session)
  return skills

@router.get("/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_202_ACCEPTED)
def get_skill_by_id(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)],
  skill_id: int
  ):
  skill = skill_service.read_skill_by_id(skill_id, session)

  if not skill:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"No se encontro la habilidad con el id {skill_id}"
      )
  
  return skill

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
  current_user: Annotated[UserResponse, Depends(get_current_user)],
  new_skill_data: SkillCreate,
  session: Annotated[Session, Depends(get_session)],
  ):

  created_skill = skill_service.create_skill(new_skill_data, session)

  if not created_skill:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="No se pudo crear la habilidad"
      )

  return created_skill
