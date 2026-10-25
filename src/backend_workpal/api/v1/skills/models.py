from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List
from ..task_with_skill.models import TaskWithSkill

if TYPE_CHECKING:
  from ..tasks.models import Tasks

class SkillsBase(SQLModel):
  name: str = Field(unique=True)

class Skills(SkillsBase, table=True):
  id: int = Field(default=None, primary_key=True)

  tasks: List["Tasks"] = Relationship(back_populates="skills", link_model=TaskWithSkill)