from sqlmodel import Session

from .models import Institutions, InstitutionCreate
from backend_workpal.database.database import save

class InstitutionService:
  def create_institution(self, institution_data: InstitutionCreate, session: Session):
    new_institution = Institutions.model_validate(institution_data)

    save(session, new_institution)

    return new_institution