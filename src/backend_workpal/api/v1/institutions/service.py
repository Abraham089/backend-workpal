from sqlmodel import Session, select
from sqlalchemy.orm import joinedload

from .models import Institutions, InstitutionCreate
from backend_workpal.database.database import save

class InstitutionService:
  def get_all_institutions(self, session:Session):
    statement = select(Institutions).options(joinedload(Institutions.users))

    institutions = session.exec(statement).unique().all()

    return institutions
  def get_institution_by_id(self, institution_id: int, session: Session):
    statement = select(Institutions).options(
      joinedload(Institutions.users)
      ).where(Institutions.id == institution_id)

    institution = session.exec(statement).unique().first()

    return institution

  def create_institution(self, institution_data: InstitutionCreate, session: Session):
    new_institution = Institutions.model_validate(institution_data)

    save(session, new_institution)

    return new_institution
