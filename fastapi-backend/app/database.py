from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import NEON_DB_HOST, NEON_DB_PORT, NEON_DB_NAME, NEON_DB_USER, NEON_DB_PASSWORD

DATABASE_URL = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}:{NEON_DB_PORT}/{NEON_DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
