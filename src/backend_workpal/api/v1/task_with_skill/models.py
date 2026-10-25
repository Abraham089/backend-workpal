from sqlmodel import SQLModel, Field

class TaskWithSkill(SQLModel, table=True):
  task_id: int | None = Field(default=None, foreign_key="tasks.id", primary_key=True)
  skill_id: int | None = Field(default=None, foreign_key="skills.id", primary_key=True)
