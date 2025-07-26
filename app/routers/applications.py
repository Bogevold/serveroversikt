from typing import Annotated
from fastapi import APIRouter, Depends, Query
from ..database import SessionDep
from ..services.application_service import ApplicationService
from ..models.application import Application

router = APIRouter(prefix="/applications", tags=["applications"])

def get_application_service(session: SessionDep) -> ApplicationService:
  """Dependency for ApplicationService"""
  return ApplicationService(session)

@router.post("/", response_model=Application.Public)
def create_application(
  application: Application.Create,
  service: ApplicationService = Depends(get_application_service)
):
  """Opprett en ny applikasjon"""
  return service.create_application(application)

@router.get("/", response_model=list[Application.Public])
def read_applications(
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
  service: ApplicationService = Depends(get_application_service)
):
  """Hent alle applikasjoner"""
  return service.get_applications(offset=offset, limit=limit)

@router.get("/{application_id}", response_model=Application.Public)
def read_application(
  application_id: int,
  service: ApplicationService = Depends(get_application_service)
):
  """Hent en spesifikk applikasjon"""
  return service.get_application(application_id)

@router.patch("/{application_id}", response_model=Application.Public)
def update_application(
  application_id: int,
  application: Application.Update,
  service: ApplicationService = Depends(get_application_service)
):
  """Oppdater en applikasjon"""
  return service.update_application(application_id, application)

@router.delete("/{application_id}")
def delete_application(
  application_id: int,
  service: ApplicationService = Depends(get_application_service)
):
  """Slett en applikasjon"""
  deleted_application = service.delete_application(application_id)
  return {"ok": True, "message": "Application deleted successfully", "application": deleted_application}
