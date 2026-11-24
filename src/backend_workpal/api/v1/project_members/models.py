from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ..users.models import Users, UserSummary
  from ..projects.models import Projects, ProjectSummary

class ProjectMembersBase(SQLModel):
  can_edit_project_details: bool = Field(default=False) 
  can_manage_tasks: bool = Field(default=True)
  can_delete_tasks: bool = Field(default=False)
  can_invite_members: bool = Field(default=False)
  is_leader: bool = Field(default=False)
  joined_at: date = Field(default_factory=lambda: date.today())

class ProjectMemberCreate(ProjectMembersBase):
  user_id: int

class ProjectMemberUpdate(SQLModel):
  can_edit_project_details: bool
  can_manage_tasks: bool
  can_delete_tasks: bool
  can_invite_members: bool

class ProjectMemberResponse(ProjectMembersBase):
  id: int
  user: "UserSummary"
  project: "ProjectSummary"
  
class ProjectMembers(ProjectMembersBase, table=True):
  id: int = Field(default=None, primary_key=True)
  __table_args__ = (UniqueConstraint("user_id", "project_id"),)

  user_id: int = Field(foreign_key="users.id", index=True)
  user: "Users" = Relationship(back_populates="project_memberships")

  project_id: int = Field(foreign_key="projects.id", index=True)
  project: "Projects" = Relationship(back_populates="members")
