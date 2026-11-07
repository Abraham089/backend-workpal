from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
  from ..users.models import Users
  from ..projects.models import Projects

class CommentsBase(SQLModel):
  content: str
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: Optional[datetime] = None

class Comments(CommentsBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  project_id: int = Field(foreign_key="projects.id", index=True)
  project: Optional["Projects"] = Relationship(back_populates="comments")

  author_id: int = Field(foreign_key="users.id", index=True)
  author: Optional["Users"] = Relationship(back_populates="comments")