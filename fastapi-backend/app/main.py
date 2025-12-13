from fastapi import FastAPI
import app.config  # Import to load environment variables
from fastapi.middleware.cors import CORSMiddleware
# from .database import engine  # Assuming this might be the import
# from .models import user  # Assuming this might be the import
from .api import auth, chatbot, history
from app.services.logger import setup_logging, logger # Import logger

# Initialize logging as early as possible
setup_logging()

# user.Base.metadata.create_all(bind=engine) # This line is causing an error

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])
app.include_router(history.router, prefix="/api", tags=["history"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.") # Example log
    return {"message": "Welcome to the Humanoid Robotics Book API"}