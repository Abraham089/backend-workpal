from sqlmodel import SQLModel, Field, Relationship, String
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from ..users.models import Users

class RolesBase(SQLModel):
  name: str = Field(unique=True, index=True, max_length=50, sa_type=String(50))

class RolesResponse(RolesBase):
  id: int

class Roles(RolesBase, table=True):
  id: int = Field(default=None, primary_key=True)

  users: List["Users"] = Relationship(back_populates="role")
