from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

# Connecting DB using sqlalchemy orm
DB_CONNECTION_URI = config("DB_CONNECTION_URI", cast=str, default=None)
engine = create_engine(DB_CONNECTION_URI)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Dependency Check
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()