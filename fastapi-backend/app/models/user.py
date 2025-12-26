from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    software_background = Column(String)
    hardware_background = Column(String)

    # Relationship to ChatSession if you want to link users to chat sessions
    # chat_sessions = relationship("ChatSession", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
