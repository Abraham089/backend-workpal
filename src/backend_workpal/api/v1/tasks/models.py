from sqlmodel import SQLModel, Relationship, Field, String
from typing import TYPE_CHECKING, Optional, List
from ..task_with_skill.models import TaskWithSkill
from datetime import date

if TYPE_CHECKING:
  from ..projects.models import Projects
  from ..users.models import Users
  from ..skills.models import Skills

class TasksBase(SQLModel):
  name: str = Field(max_length=40, sa_type=String(40))
  description: str = Field(max_length=200, sa_type=String(200))
  status: str = Field(max_length=15, sa_type=String(15))
  end_date: date

class Tasks(TasksBase, table=True):
  id: int = Field(default=None, primary_key=True)

  project_id: int = Field(foreign_key="projects.id")
  project: "Projects" = Relationship(back_populates="tasks")

  user_id: int = Field(foreign_key="users.id")
  assigned_user: Optional["Users"] = Relationship(back_populates="tasks")

  skills: List["Skills"] = Relationship(back_populates="tasks", link_model=TaskWithSkill)