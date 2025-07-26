from fastapi import HTTPException
from sqlmodel import Session, select
from ..models.installation import Installation

class InstallationService:
  """Service klasse for installasjon operasjoner"""
  
  def __init__(self, session: Session):
    self.session = session
  
  def create_installation(self, installation_data: Installation.Create) -> Installation:
    """Opprett en ny installasjon"""
    db_installation = Installation.model_validate(installation_data)
    self.session.add(db_installation)
    self.session.commit()
    self.session.refresh(db_installation)
    return db_installation
  
  def get_installations(self, offset: int = 0, limit: int = 100) -> list[Installation]:
    """Hent alle installasjoner med paginering"""
    installations = self.session.exec(
      select(Installation).offset(offset).limit(limit)
    ).all()
    return installations
  
  def get_installation(self, application_id: int, server_id: int) -> Installation:
    """Hent en spesifikk installasjon basert på sammensatt nøkkel"""
    installation = self.session.exec(
      select(Installation).where(
        Installation.application_id == application_id,
        Installation.server_id == server_id
      )
    ).first()
    if not installation:
      raise HTTPException(status_code=404, detail="Installation not found")
    return installation
  
  def get_installations_by_server(self, server_id: int) -> list[Installation]:
    """Hent alle installasjoner for en spesifikk server"""
    installations = self.session.exec(
      select(Installation).where(Installation.server_id == server_id)
    ).all()
    return installations
  
  def get_installations_by_application(self, application_id: int) -> list[Installation]:
    """Hent alle installasjoner for en spesifikk applikasjon"""
    installations = self.session.exec(
      select(Installation).where(Installation.application_id == application_id)
    ).all()
    return installations
  
  def update_installation(self, application_id: int, server_id: int, installation_data: Installation.Update) -> Installation:
    """Oppdater en installasjon"""
    db_installation = self.session.exec(
      select(Installation).where(
        Installation.application_id == application_id,
        Installation.server_id == server_id
      )
    ).first()
    if not db_installation:
      raise HTTPException(status_code=404, detail="Installation not found")
    
    installation_update_data = installation_data.model_dump(exclude_unset=True)
    db_installation.sqlmodel_update(installation_update_data)
    self.session.add(db_installation)
    self.session.commit()
    self.session.refresh(db_installation)
    return db_installation
  
  def delete_installation(self, application_id: int, server_id: int) -> Installation:
    """Slett en installasjon"""
    db_installation = self.session.exec(
      select(Installation).where(
        Installation.application_id == application_id,
        Installation.server_id == server_id
      )
    ).first()
    if not db_installation:
      raise HTTPException(status_code=404, detail="Installation not found")
    
    self.session.delete(db_installation)
    self.session.commit()
    return db_installation
