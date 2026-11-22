from sqlmodel import SQLModel, Field, Relationship, String
from typing import TYPE_CHECKING, List, Optional
from datetime import date

from ..users.models import UserSummary
from ..comments.models import CommentResponse

if TYPE_CHECKING:
  from ..users.models import Users
  from ..tasks.models import Tasks
  from ..project_members.models import ProjectMembers, ProjectMemberResponse
  from ..comments.models import Comments
  from ..project_join_requests.models import ProjectJoinRequests

class ProjectsBase(SQLModel):
  name: str = Field(unique=True, max_length=40)
  description: str = Field(max_length=200, sa_type=String(200))
  img: str
  created_at: date = Field(default_factory=lambda: date.today())
  status: str = Field(max_length=15, sa_type=String(15))
  ending_date: date

class ProjectCreate(ProjectsBase):
  created_by_id: int
  supervisor_user_id: Optional[int] = None

class ProjectUpdate(ProjectsBase):
  created_by_id: int
  supervisor_user_id: Optional[int] = None

class ProjectResponse(ProjectsBase):
  id: int
  created_by: UserSummary
  supervisor_user: Optional[UserSummary] = None
  members: List["ProjectMemberResponse"]

class ProjectSummary(ProjectsBase):
  id: int

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

  members: List["ProjectMembers"] = Relationship(
    back_populates="project",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

  tasks: List["Tasks"] = Relationship(
    back_populates="project",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"})

  comments: List["Comments"] = Relationship(
    back_populates="project",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
  
  join_requests: List["ProjectJoinRequests"] = Relationship(
      back_populates="project",
      sa_relationship_kwargs={"cascade": "all, delete-orphan"}
  )
