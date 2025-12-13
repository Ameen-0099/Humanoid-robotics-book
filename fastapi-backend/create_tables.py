import asyncio
from sqlalchemy.exc import ProgrammingError
from app.database import async_engine, Base
from app.models.chat import ChatSession, ChatMessage  # Import your models

async def init_db():
    """
    Asynchronously creates all tables in the database defined by the Base metadata.
    Handles cases where tables already exist.
    """
    async with async_engine.begin() as conn:
        try:
            # The `run_sync` method is used to execute a synchronous function (like create_all)
            # within an asynchronous context.
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created successfully.")
        except ProgrammingError as e:
            # This error is expected if the tables already exist.
            if "already exists" in str(e):
                print("Database tables already exist.")
            else:
                # If it's a different programming error, raise it.
                raise

if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())
