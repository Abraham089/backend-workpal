from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from ..roles.models import Roles
  from ..projects.models import Projects
  from ..tasks.models import Tasks

class UsersBase(SQLModel):
  name: str
  last_name: str
  username: str = Field(unique=True)
  is_active: bool = True

class Users(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  password_hash: str

  role_id: int = Field(foreign_key="roles.id")
  role: "Roles" = Relationship(back_populates="users")

  projects: List["Projects"] = Relationship(back_populates="user")
  tasks: List["Tasks"] = Relationship(back_populates="assigned_user")
