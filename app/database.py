from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Database konfigurasjon
pg_user = "srv_sian"
pg_password = "passordetErHemmelig"
pg_host = "localhost"
pg_port = 5432
pg_db = "serveroversikt"
postgres_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

engine = create_engine(postgres_url)

def create_db_and_tables():
  """Opprett database tabeller"""
  SQLModel.metadata.create_all(engine)

def get_session():
  """Database session dependency"""
  with Session(engine) as session:
    yield session

SessionDep = Annotated[Session, Depends(get_session)]
