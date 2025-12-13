import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models.user import Base, User


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Required for in-memory DB with multiple connections
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

def test_create_user_signup():
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200 # Assuming 200 for successful creation, check schema if 201 expected
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

    # Verify user exists in the database
    db = TestingSessionLocal()
    user_in_db = db.query(User).filter(User.email == "test@example.com").first()
    assert user_in_db is not None
    assert user_in_db.username == "testuser"
    db.close()

def test_create_user_duplicate_email():
    # First user creation (should already exist from previous test if tests run sequentially)
    client.post(
        "/auth/signup",
        json={"username": "anotheruser", "email": "duplicate@example.com", "password": "testpassword"},
    )
    # Attempt to create user with duplicate email
    response = client.post(
        "/auth/signup",
        json={"username": "yetanotheruser", "email": "duplicate@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_user_duplicate_username():
    # First user creation
    client.post(
        "/auth/signup",
        json={"username": "duplicateusername", "email": "unique1@example.com", "password": "testpassword"},
    )
    # Attempt to create user with duplicate username
    response = client.post(
        "/auth/signup",
        json={"username": "duplicateusername", "email": "unique2@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]
