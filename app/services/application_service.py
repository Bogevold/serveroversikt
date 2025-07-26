from fastapi import HTTPException
from sqlmodel import Session, select
from ..models.application import Application

class ApplicationService:
  """Service klasse for applikasjon operasjoner"""
  
  def __init__(self, session: Session):
    self.session = session
  
  def create_application(self, application_data: Application.Create) -> Application:
    """Opprett en ny applikasjon"""
    db_application = Application.model_validate(application_data)
    self.session.add(db_application)
    self.session.commit()
    self.session.refresh(db_application)
    return db_application
  
  def get_applications(self, offset: int = 0, limit: int = 100) -> list[Application]:
    """Hent alle applikasjoner med paginering"""
    applications = self.session.exec(
      select(Application).offset(offset).limit(limit)
    ).all()
    return applications
  
  def get_application(self, application_id: int) -> Application:
    """Hent en spesifikk applikasjon"""
    application = self.session.get(Application, application_id)
    if not application:
      raise HTTPException(status_code=404, detail="Application not found")
    return application
  
  def update_application(self, application_id: int, application_data: Application.Update) -> Application:
    """Oppdater en applikasjon"""
    db_application = self.session.get(Application, application_id)
    if not db_application:
      raise HTTPException(status_code=404, detail="Application not found")
    
    application_update_data = application_data.model_dump(exclude_unset=True)
    db_application.sqlmodel_update(application_update_data)
    self.session.add(db_application)
    self.session.commit()
    self.session.refresh(db_application)
    return db_application
  
  def delete_application(self, application_id: int) -> Application:
    """Slett en applikasjon"""
    db_application = self.session.get(Application, application_id)
    if not db_application:
      raise HTTPException(status_code=404, detail="Application not found")
    
    self.session.delete(db_application)
    self.session.commit()
    return db_application
