from sqlmodel import SQLModel, Field, Relationship, String
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
  from ..users.models import Users
  from ..projects.models import Projects

class CommentsBase(SQLModel):
  content: str = Field(max_length=50, sa_type=String(50))
  created_at: date = Field(default_factory=lambda: date.today())
  updated_at: Optional[date] = None

class Comments(CommentsBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  project_id: int = Field(foreign_key="projects.id", index=True)
  project: Optional["Projects"] = Relationship(back_populates="comments")

  author_id: int = Field(foreign_key="users.id", index=True)
  author: Optional["Users"] = Relationship(back_populates="comments")