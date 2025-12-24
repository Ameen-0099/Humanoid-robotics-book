import asyncio
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from app.database import async_engine, Base
from app.models.chat import ChatSession, ChatMessage  # Import your models

async def create_better_auth_tables():
    """
    Creates the tables required by Better Auth.
    """
    sql_file = "better-auth_migrations/2025-12-20T06-25-48.035Z.sql"
    with open(sql_file, "r") as f:
        sql_commands = f.read()

    commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]

    async with async_engine.connect() as conn:
        for command in commands:
            try:
                # Wrap each command in its own transaction
                async with conn.begin():
                    await conn.execute(text(command))
            except ProgrammingError as e:
                if "already exists" in str(e) or "duplicate" in str(e):
                    print(f"Table/Index already exists, skipping command.")
                    # The transaction is automatically rolled back on exception
                else:
                    raise

    print("Better Auth tables created successfully.")


async def add_missing_user_columns():
    """
    Manually adds missing columns to the 'users' table.
    """
    async with async_engine.connect() as conn:
        async with conn.begin():
            try:
                await conn.execute(text('ALTER TABLE users ADD COLUMN software_background VARCHAR;'))
                print("Added 'software_background' column to 'users' table.")
            except ProgrammingError as e:
                if 'column "software_background" of relation "users" already exists' in str(e):
                    print("Column 'software_background' already exists.")
                else:
                    raise
            try:
                await conn.execute(text('ALTER TABLE users ADD COLUMN hardware_background VARCHAR;'))
                print("Added 'hardware_background' column to 'users' table.")
            except ProgrammingError as e:
                if 'column "hardware_background" of relation "users" already exists' in str(e):
                    print("Column 'hardware_background' already exists.")
                else:
                    raise


async def init_db():
    """
    Asynchronously creates all tables in the database defined by the Base metadata.
    Handles cases where tables already exist.
    """
    await create_better_auth_tables()
    await add_missing_user_columns()
    async with async_engine.begin() as conn:
        # The `run_sync` method is used to execute a synchronous function (like create_all)
        # within an asynchronous context.
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables applied successfully.")


if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())
