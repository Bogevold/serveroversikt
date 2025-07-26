from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import servers_router, applications_router, installations_router

# Import models for SQLModel metadata
from .models import Server, Application, Installation

app = FastAPI(
  title="Server Oversikt API",
  description="API for å administrere servere, applikasjoner og installasjoner",
  version="1.0.0"
)

# Inkluder routere
app.include_router(servers_router)
app.include_router(applications_router)
app.include_router(installations_router)

@app.on_event("startup")
def on_startup():
  """Opprett database tabeller ved oppstart"""
  create_db_and_tables()

@app.get("/")
def root():
  """Root endpoint"""
  return {"message": "Server Oversikt API"}