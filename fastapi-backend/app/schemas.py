from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    software_background: str | None = None
    hardware_background: str | None = None

class UserLogin(BaseModel): # New schema for login
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str # Keep username for display/internal use if needed
    email: str
    software_background: str | None = None
    hardware_background: str | None = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None