from sqlmodel import Session, create_engine
from config.config import settings

# engine = create_engine(settings.database_url, echo=True)
engine = create_engine(f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:5432/{settings.database_name}", echo=True)

def get_session():
    with Session(engine) as session:
        yield session

