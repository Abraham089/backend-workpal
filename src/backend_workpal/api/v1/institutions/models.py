from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List
from ..institution_with_user.models import InstitutionWithUser

from ..users.models import UserSummary

if TYPE_CHECKING:
  from ..users.models import Users

class InstitutionBase(SQLModel):
  name: str = Field(unique=True)
  description: str = Field(max_length=500)
  color: str = Field(max_length=6)
  logo: str = Field(unique=True)

class InstitutionCreate(InstitutionBase):
  pass

class InstitutionResponse(InstitutionBase):
  id: int
  users: List[UserSummary]

class Institutions(InstitutionBase, table=True):
  id: int = Field(default=None, primary_key=True)

  users: List["Users"] = Relationship(back_populates="institutions", link_model=InstitutionWithUser)
