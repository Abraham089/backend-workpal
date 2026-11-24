from sqlmodel import SQLModel, Field, Relationship, String
from typing import TYPE_CHECKING, List, Optional
from datetime import date
from ..users.models import UserResponse
from enum import Enum
from pydantic import FutureDate,field_validator,model_validator

if TYPE_CHECKING:
  from ..users.models import Users
  from ..tasks.models import Tasks
  from ..project_members.models import ProjectMembers
  from ..comments.models import Comments


class ProjectStatus(str, Enum):
  ACTIVE = "Active"
  PAUSED = "Paused"
  FINISHED = "Finished"
  
class ProjectsBase(SQLModel):
  name: str = Field(unique=True, max_length=40)
  description: str = Field(max_length=200, sa_type=String(200))
  img: str
  created_at: date = Field(default_factory=lambda: date.today())
  status: ProjectStatus = Field( sa_type=String(15))
  ending_date: date
  
  

class ProjectCreate(ProjectsBase):
  ending_date: FutureDate
  supervisor_user_id: Optional[int] = None
  

class ProjectUpdate(SQLModel):
  name: Optional[str] = Field(default=None, max_length=40)
  description: Optional[str] = Field(default=None, max_length=200)
  img: Optional[str] = None
  status: Optional[ProjectStatus] = None
  ending_date: Optional[date] = None
  supervisor_user_id: Optional[int] = None

class ProjectResponse(ProjectsBase):
  id: int
  created_by: UserResponse
  supervisor_user: Optional[UserResponse] = None

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

  members: List["ProjectMembers"] = Relationship(back_populates="project", cascade_delete=True)

  tasks: List["Tasks"] = Relationship(back_populates="project", cascade_delete=True)

  comments: List["Comments"] = Relationship(back_populates="project", cascade_delete=True)
