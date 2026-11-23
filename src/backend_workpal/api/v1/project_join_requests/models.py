from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional, TYPE_CHECKING
from datetime import date
from enum import Enum
from ..users.models import Users, UserSummary
from ..projects.models import Projects, ProjectSummary

class JoinRequestStatus(str, Enum):
  PENDING = "pending"
  ACCEPTED = "accepted"
  REJECTED = "rejected"

class ProjectJoinRequestsBase(SQLModel):
  message: Optional[str] = Field(default=None, max_length=200)
  status: JoinRequestStatus = Field(default=JoinRequestStatus.PENDING)
  created_at: date = Field(default_factory=lambda: date.today())

class ProjectJoinRequestCreate(SQLModel):
  message: Optional[str] = Field(default=None, max_length=200)

class ProjectJoinRequestUpdate(SQLModel):
  status: JoinRequestStatus

class ProjectJoinRequestResponse(ProjectJoinRequestsBase):
  id: int
  user: "UserSummary"
  project: "ProjectSummary"

class ProjectJoinRequests(ProjectJoinRequestsBase, table=True):
  id: int = Field(default=None, primary_key=True)
  __table_args__ = (UniqueConstraint("user_id", "project_id"),)

  user_id: int = Field(foreign_key="users.id", index=True)
  user: "Users" = Relationship(back_populates="join_requests")

  project_id: int = Field(foreign_key="projects.id", index=True)
  project: "Projects" = Relationship(back_populates="join_requests")
