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
    skills = select(Skills)
    return session.exec(skills).all()

  def create_skill(self, new_skill_data: SkillCreate, session:Session):
    new_skill = Skills(
      name=new_skill_data.name
    )
    saved_skill = save(session, new_skill)
    return saved_skill
