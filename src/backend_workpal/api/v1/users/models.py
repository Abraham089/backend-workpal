from sqlmodel import SQLModel, Field, Relationship, String
from typing import TYPE_CHECKING, List
from pydantic import EmailStr

if TYPE_CHECKING:
  from ..roles.models import Roles
  from ..projects.models import Projects
  from ..tasks.models import Tasks
  from ..project_members.models import ProjectMembers
  from ..comments.models import Comments

class UsersBase(SQLModel):
  enrollment: str | None = Field(unique=True)
  name: str = Field(max_length=50, sa_type=String(50))
  last_name: str = Field(max_length=50, sa_type=String(50))
  username: str = Field(unique=True, max_length=30, sa_type=String(30))
  mail: EmailStr = Field(unique=True, max_length=50, sa_type=String(50))
  is_active: bool = True

class UserCreate(UsersBase):
  password: str
  rol_id: int

class Users(UsersBase, table=True):
  id: int = Field(default=None, primary_key=True)
  password_hash: str

  role_id: int = Field(foreign_key="roles.id")
  role: "Roles" = Relationship(back_populates="users")

  project_memberships: List["ProjectMembers"] = Relationship(back_populates="user")

  created_projects: List["Projects"] = Relationship(
    back_populates="created_by",
    sa_relationship_kwargs={"foreign_keys": "Projects.created_by_id"}
    )

  supervised_projects: List["Projects"] = Relationship(
    back_populates="supervisor_user",
    sa_relationship_kwargs={"foreign_keys": "Projects.supervisor_user_id"}
    )

  tasks: List["Tasks"] = Relationship(back_populates="assigned_user")

  comments: List["Comments"] = Relationship(back_populates="author")
