from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .application import Application
  from .server import Server

class Installation(SQLModel, table=True):
  """Installation modell - mange-til-mange relasjon mellom Application og Server"""
  application_id: int = Field(foreign_key="application.id", primary_key=True)
  server_id: int = Field(foreign_key="server.id", primary_key=True)
  version: str
  
  application: Application = Relationship(back_populates="installations")
  server: Server = Relationship(back_populates="installations")

  class Base(SQLModel):
    """Base klasse for Installation schemas"""
    application_id: int
    server_id: int
    version: str

  class Create(Base):
    """Schema for å opprette en installasjon"""
    pass

  class Update(SQLModel):
    """Schema for å oppdatere en installasjon"""
    version: str | None = None

  class Public(Base):
    """Schema for offentlig installasjon representasjon"""
    pass
