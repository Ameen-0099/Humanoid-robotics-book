from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None
    software_background: str | None = None
    hardware_background: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    software_background: str | None = None
    hardware_background: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDisplay(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None