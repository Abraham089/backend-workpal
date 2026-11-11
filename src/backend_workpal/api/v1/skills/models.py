from sqlmodel import SQLModel, Field, Relationship, String
from typing import TYPE_CHECKING, List
from ..task_with_skill.models import TaskWithSkill

if TYPE_CHECKING:
  from ..tasks.models import Tasks

class SkillsBase(SQLModel):
  name: str = Field(unique=True, max_length=50, sa_type=String(50))

class SkillCreate(SkillsBase):
  pass

class SkillResponse(SkillsBase):
  id: int

class Skills(SkillsBase, table=True):
  id: int = Field(default=None, primary_key=True)

  tasks: List["Tasks"] = Relationship(back_populates="skills", link_model=TaskWithSkill)