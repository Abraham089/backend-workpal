from sqlmodel import Session, select, col
from sqlalchemy.orm import joinedload
from .models import Skills, SkillCreate
from typing import List
from backend_workpal.database.database import save

class SkillService:
  def read_skill_by_id(self, skill_id:int, session: Session):
    statement = select(Skills).where(Skills.id == skill_id)
    skill = session.exec(statement).first()
      
    return skill

  def read_all_skills(self, session: Session):
    users = select(Skills)
    return session.exec(users).all()
