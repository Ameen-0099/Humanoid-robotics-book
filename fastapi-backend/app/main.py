import requests
from fastapi import FastAPI
import app.config  # Import to load environment variables
from fastapi.middleware.cors import CORSMiddleware
from app.database import async_engine, Base
from app.api import chatbot, history, auth
from app.services.logger import setup_logging, logger # Re-Import logger

# Initialize logging as early as possible
setup_logging()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        # Create all tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])
app.include_router(history.router, prefix="/api", tags=["history"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.") # Example log
    return {"message": "Welcome to the Humanoid Robotics Book API"}