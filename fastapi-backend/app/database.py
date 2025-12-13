from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import NEON_DATABASE_URL

# Create an asynchronous engine
async_engine = create_async_engine(
    NEON_DATABASE_URL,
    pool_pre_ping=True,
    echo=False, # Set to True to see SQL queries
)

# Create a session maker for asynchronous sessions
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Base class for declarative models
Base = declarative_base()

async def get_db_session():
    """
    Dependency to get an async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
