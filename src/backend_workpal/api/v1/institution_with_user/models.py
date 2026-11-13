from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List

class InstitutionWithUser(SQLModel, table=True):
  institution_id: int | None = Field(default=None, foreign_key="institutions.id", primary_key=True)
  user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
