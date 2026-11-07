from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ..users.models import Users
  from ..projects.models import Projects

class ProjectMembersBase(SQLModel):
  can_edit_project_details: bool = Field(default=False) 
  can_manage_tasks: bool = Field(default=True)
  can_delete_tasks: bool = Field(default=False)
  can_invite_members: bool = Field(default=False)
  is_leader: bool = Field(default=False)
  joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  
class ProjectMembers(ProjectMembersBase, table=True):
  id: int = Field(default=None, primary_key=True)

  user_id: int = Field(foreign_key="users.id", index=True)
  user: Optional["Users"] = Relationship(back_populates="project_memberships")

  project_id: int = Field(foreign_key="projects.id", index=True)
  project: Optional["Projects"] = Relationship(back_populates="members")

