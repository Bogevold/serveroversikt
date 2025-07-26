from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .installation import Installation

class Server(SQLModel, table=True):
  """Server modell for database"""
  id: int = Field(default=None, primary_key=True)
  name: str
  location: str
  installations: list[Installation] = Relationship(back_populates="server")

  class Base(SQLModel):
    """Base klasse for Server schemas"""
    name: str
    location: str

  class Create(Base):
    """Schema for å opprette en server"""
    pass

  class Update(SQLModel):
    """Schema for å oppdatere en server"""
    name: str | None = None
    location: str | None = None

  class Public(Base):
    """Schema for offentlig server representasjon"""
    id: int
