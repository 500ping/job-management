import urllib.parse
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.configs.setting import get_settings

# Get application settings
settings = get_settings()
encoded_password = urllib.parse.quote_plus(settings.db_password)

# Create the connection URL
DATABASE_URL = f"postgresql://{settings.db_user}:{encoded_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Check connection validity before using it
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Maximum overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=True,
    connect_args={"options": f"-csearch_path={settings.db_schema},public"},
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

# Create a base class for declarative models
Base = declarative_base(metadata=MetaData(schema=settings.db_schema))


@contextmanager
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Session:
    """Get a database session."""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise Exception(f"Database connection error: {e}")
