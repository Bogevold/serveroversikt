from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .installation import Installation

class Application(SQLModel, table=True):
  """Application modell for database"""
  id: int = Field(default=None, primary_key=True)
  name: str
  description: str | None = None
  installations: list[Installation] = Relationship(back_populates="application")

  class Base(SQLModel):
    """Base klasse for Application schemas"""
    name: str
    description: str | None = None

  class Create(Base):
    """Schema for å opprette en applikasjon"""
    pass

  class Update(SQLModel):
    """Schema for å oppdatere en applikasjon"""
    name: str | None = None
    description: str | None = None
    server_id: int | None = None

  class Public(Base):
    """Schema for offentlig applikasjon representasjon"""
    id: int
