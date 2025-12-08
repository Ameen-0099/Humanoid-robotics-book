from fastapi import FastAPI
from .api import auth
from .database import engine
from .models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"Hello": "World"}