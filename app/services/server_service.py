from typing import Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from ..models.server import Server

class ServerService:
  """Service klasse for server operasjoner"""
  
  def __init__(self, session: Session):
    self.session = session
  
  def create_server(self, server_data: Server.Create) -> Server:
    """Opprett en ny server"""
    db_server = Server.model_validate(server_data)
    self.session.add(db_server)
    self.session.commit()
    self.session.refresh(db_server)
    return db_server
  
  def get_servers(self, offset: int = 0, limit: int = 100) -> list[Server]:
    """Hent alle servere med paginering"""
    servers = self.session.exec(
      select(Server).offset(offset).limit(limit)
    ).all()
    return servers
  
  def get_server(self, server_id: int) -> Server:
    """Hent en spesifikk server"""
    server = self.session.get(Server, server_id)
    if not server:
      raise HTTPException(status_code=404, detail="Server not found")
    return server
  
  def update_server(self, server_id: int, server_data: Server.Update) -> Server:
    """Oppdater en server"""
    db_server = self.session.get(Server, server_id)
    if not db_server:
      raise HTTPException(status_code=404, detail="Server not found")
    
    server_update_data = server_data.model_dump(exclude_unset=True)
    db_server.sqlmodel_update(server_update_data)
    self.session.add(db_server)
    self.session.commit()
    self.session.refresh(db_server)
    return db_server
  
  def delete_server(self, server_id: int) -> Server:
    """Slett en server"""
    db_server = self.session.get(Server, server_id)
    if not db_server:
      raise HTTPException(status_code=404, detail="Server not found")
    
    self.session.delete(db_server)
    self.session.commit()
    return db_server
