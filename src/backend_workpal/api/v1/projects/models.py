from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ..users.models import Users
  from ..tasks.models import Tasks

class ProjectsBase(SQLModel):
  name: str = Field(unique=True)
  description: str
  img: str

class Projects(ProjectsBase, table=True):
  id: int = Field(default=None, primary_key=True)

  user_leader_id: int = Field(foreign_key="users.id")
  user_leader: "Users" = Relationship(back_populates="projects")

  tasks: "Tasks" = Relationship(back_populates="project")
