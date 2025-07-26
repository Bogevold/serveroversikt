from typing import Annotated
from fastapi import APIRouter, Depends, Query
from ..database import SessionDep
from ..services.server_service import ServerService
from ..models.server import Server

router = APIRouter(prefix="/servers", tags=["servers"])

def get_server_service(session: SessionDep) -> ServerService:
  """Dependency for ServerService"""
  return ServerService(session)

@router.post("/", response_model=Server.Public)
def create_server(
  server: Server.Create,
  service: ServerService = Depends(get_server_service)
):
  """Opprett en ny server"""
  return service.create_server(server)

@router.get("/", response_model=list[Server.Public])
def read_servers(
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
  service: ServerService = Depends(get_server_service)
):
  """Hent alle servere"""
  return service.get_servers(offset=offset, limit=limit)

@router.get("/{server_id}", response_model=Server.Public)
def read_server(
  server_id: int,
  service: ServerService = Depends(get_server_service)
):
  """Hent en spesifikk server"""
  return service.get_server(server_id)

@router.patch("/{server_id}", response_model=Server.Public)
def update_server(
  server_id: int,
  server: Server.Update,
  service: ServerService = Depends(get_server_service)
):
  """Oppdater en server"""
  return service.update_server(server_id, server)

@router.delete("/{server_id}")
def delete_server(
  server_id: int,
  service: ServerService = Depends(get_server_service)
):
  """Slett en server"""
  deleted_server = service.delete_server(server_id)
  return {"ok": True, "message": "Server deleted successfully", "server": deleted_server}
