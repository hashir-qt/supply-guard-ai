from sqlmodel import create_engine, Session, SQLModel
from backend.config import get_settings

settings = get_settings()

db_url = settings.DATABASE_URL

# Create Engine
engine = create_engine(db_url, echo=settings.DEBUG)

def init_db():
    """Create all tables defined in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to provide a DB session."""
    with Session(engine) as session:
        yield session
