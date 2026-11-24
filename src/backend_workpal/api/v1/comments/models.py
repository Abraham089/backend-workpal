from sqlmodel import SQLModel, Field, Relationship, String
from typing import Optional, TYPE_CHECKING, List
from datetime import date

if TYPE_CHECKING:
  from ..users.models import Users
  from ..projects.models import Projects
  from ..tasks.models import Tasks

class CommentsBase(SQLModel):
  content: str = Field(max_length=50, sa_type=String(50))
  created_at: date = Field(default_factory=lambda: date.today())
  updated_at: Optional[date] = None

class CommentResponse(CommentsBase):
  id: int

class Comments(CommentsBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  project_id: Optional[int] = Field(default=None, foreign_key="projects.id", index=True)
  project: Optional["Projects"] = Relationship(back_populates="comments")

  task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", index=True)
  task: Optional["Tasks"] = Relationship(back_populates="comments")

  author_id: int = Field(foreign_key="users.id", index=True)
  author: Optional["Users"] = Relationship(back_populates="comments")
