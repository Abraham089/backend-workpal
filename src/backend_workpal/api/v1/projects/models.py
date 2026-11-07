from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone

if TYPE_CHECKING:
  from ..users.models import Users
  from ..tasks.models import Tasks
  from ..project_members.models import ProjectMembers
  from ..comments.models import Comments

class ProjectsBase(SQLModel):
  name: str = Field(unique=True)
  description: str
  img: str
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Projects(ProjectsBase, table=True):
  id: int = Field(default=None, primary_key=True)

  created_by_id: int = Field(foreign_key="users.id")
  created_by: "Users" = Relationship(
    back_populates="created_projects",
    sa_relationship_kwargs={"foreign_keys": "[Projects.created_by_id]"}
    )

  supervisor_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
  supervisor_user: Optional["Users"] = Relationship(
    back_populates="supervised_projects",
    sa_relationship_kwargs={"foreign_keys": "[Projects.supervisor_user_id]"}
    )

  members: List["ProjectMembers"] = Relationship(back_populates="project")

  tasks: List["Tasks"] = Relationship(back_populates="project")

  comments: List["Comments"] = Relationship(back_populates="project")
