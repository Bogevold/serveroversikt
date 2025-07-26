from typing import Annotated
from fastapi import APIRouter, Depends, Query
from ..database import SessionDep
from ..services.installation_service import InstallationService
from ..models.installation import Installation

router = APIRouter(prefix="/installations", tags=["installations"])

def get_installation_service(session: SessionDep) -> InstallationService:
  """Dependency for InstallationService"""
  return InstallationService(session)

@router.post("/", response_model=Installation.Public)
def create_installation(
  installation: Installation.Create,
  service: InstallationService = Depends(get_installation_service)
):
  """Opprett en ny installasjon"""
  return service.create_installation(installation)

@router.get("/", response_model=list[Installation.Public])
def read_installations(
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
  service: InstallationService = Depends(get_installation_service)
):
  """Hent alle installasjoner"""
  return service.get_installations(offset=offset, limit=limit)

@router.get("/{application_id}/{server_id}", response_model=Installation.Public)
def read_installation(
  application_id: int,
  server_id: int,
  service: InstallationService = Depends(get_installation_service)
):
  """Hent en spesifikk installasjon"""
  return service.get_installation(application_id, server_id)

@router.get("/by-server/{server_id}", response_model=list[Installation.Public])
def read_installations_by_server(
  server_id: int,
  service: InstallationService = Depends(get_installation_service)
):
  """Hent alle installasjoner for en spesifikk server"""
  return service.get_installations_by_server(server_id)

@router.get("/by-application/{application_id}", response_model=list[Installation.Public])
def read_installations_by_application(
  application_id: int,
  service: InstallationService = Depends(get_installation_service)
):
  """Hent alle installasjoner for en spesifikk applikasjon"""
  return service.get_installations_by_application(application_id)

@router.patch("/{application_id}/{server_id}", response_model=Installation.Public)
def update_installation(
  application_id: int,
  server_id: int,
  installation: Installation.Update,
  service: InstallationService = Depends(get_installation_service)
):
  """Oppdater en installasjon"""
  return service.update_installation(application_id, server_id, installation)

@router.delete("/{application_id}/{server_id}")
def delete_installation(
  application_id: int,
  server_id: int,
  service: InstallationService = Depends(get_installation_service)
):
  """Slett en installasjon"""
  deleted_installation = service.delete_installation(application_id, server_id)
  return {"ok": True, "message": "Installation deleted successfully", "installation": deleted_installation}
