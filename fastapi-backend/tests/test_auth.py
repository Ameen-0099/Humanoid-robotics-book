import sys
import os
import pytest 
import unittest.mock 
from unittest.mock import AsyncMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, Depends, HTTPException, APIRouter 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import auth 
from app.database import get_db_session, Base
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Fixture to create a new engine and session for each test, and handle table creation/dropping
@pytest.fixture(name="db_session")
def db_session_fixture():
    test_engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool, 
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    Base.metadata.create_all(bind=test_engine) # Create tables for this specific test DB

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine) # Drop tables after this specific test DB

# Fixture to override the get_db_session dependency in the FastAPI app
@pytest.fixture
def override_get_db_dependency(db_session):
    _test_app.dependency_overrides[get_db_session] = lambda: db_session
    yield
    _test_app.dependency_overrides.pop(get_db_session) # Clean up the override

# Fixture to ensure database setup and teardown runs for each test and provides mock httpx client
@pytest.fixture(name="session")
def session_fixture(override_get_db_dependency, mock_httpx_client):
    yield

@pytest.fixture
def mock_httpx_client():
    with unittest.mock.patch('httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance

# Create a test FastAPI app that only includes the auth router
_test_app = FastAPI() 
_test_app.include_router(auth.router, prefix="/api/auth") 

# Client for the test app (will use the overridden dependencies)
client = TestClient(_test_app) 


def test_create_user_signup(session, mock_httpx_client, db_session): # Added db_session
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "testuser", "email": "test@example.com"}
    mock_httpx_client.post.return_value = mock_response

    response = client.post(
        "/api/auth/signup", 
        data={"name": "testuser", "email": "test@example.com", "password": "testpassword", "softwareBackground": "Test", "hardwareBackground": "Test"}, 
    )
    assert response.status_code == 200 
    data = response.json()
    assert data["name"] == "testuser" 
    assert data["email"] == "test@example.com"
    assert "id" in data

    # Verify user exists in the database
    user_in_db = db_session.query(User).filter(User.email == "test@example.com").first() # Use db_session
    assert user_in_db is not None
    assert user_in_db.username == "testuser" 

def test_create_user_duplicate_email(session, mock_httpx_client): 
    # Mock the initial signup
    mock_signup_response = AsyncMock()
    mock_signup_response.status_code = 200
    mock_signup_response.json.return_value = {"id": 1, "name": "anotheruser", "email": "duplicate@example.com"}
    mock_httpx_client.post.return_value = mock_signup_response
    
    client.post(
        "/api/auth/signup", 
        data={"name": "anotheruser", "email": "duplicate@example.com", "password": "testpassword", "softwareBackground": "Test", "hardwareBackground": "Test"}, 
    )

    # Mock the duplicate signup response
    mock_duplicate_response = AsyncMock()
    mock_duplicate_response.status_code = 400
    mock_duplicate_response.json.return_value = {"detail": "Signup failed"}
    mock_httpx_client.post.return_value = mock_duplicate_response

    response = client.post(
        "/api/auth/signup", 
        data={"name": "yetanotheruser", "email": "duplicate@example.com", "password": "testpassword", "softwareBackground": "Test", "hardwareBackground": "Test"}, 
    )
    assert response.status_code == 400
    assert "Signup failed" in response.json()["detail"] 

def test_create_user_duplicate_username(session, mock_httpx_client): 
    # Mock the initial signup
    mock_signup_response = AsyncMock()
    mock_signup_response.status_code = 200
    mock_signup_response.json.return_value = {"id": 1, "name": "duplicateusername", "email": "unique1@example.com"}
    mock_httpx_client.post.return_value = mock_signup_response

    client.post(
        "/api/auth/signup", 
        data={"name": "duplicateusername", "email": "unique1@example.com", "password": "testpassword", "softwareBackground": "Test", "hardwareBackground": "Test"}, 
    )
    
    # Mock the duplicate signup response
    mock_duplicate_response = AsyncMock()
    mock_duplicate_response.status_code = 400
    mock_duplicate_response.json.return_value = {"detail": "Signup failed"}
    mock_httpx_client.post.return_value = mock_duplicate_response

    response = client.post(
        "/api/auth/signup", 
        data={"name": "duplicateusername", "email": "unique2@example.com", "password": "testpassword", "softwareBackground": "Test", "hardwareBackground": "Test"}, 
    )
    assert response.status_code == 400
    assert "Signup failed" in response.json()["detail"] 

def test_login_for_access_token_password_grant(session, mock_httpx_client): 
    # Mock the initial signup call from the test
    mock_signup_response = AsyncMock()
    mock_signup_response.status_code = 200
    mock_signup_response.json.return_value = {"id": 1, "name": "tokenuser", "email": "token@example.com"}
    mock_httpx_client.post.return_value = mock_signup_response

    # First, create a user
    client.post(
        "/api/auth/signup",
        data={"name": "tokenuser", "email": "token@example.com", "password": "tokenpassword", "softwareBackground": "Test", "hardwareBackground": "Test"},
    )

    # Mock the internal login call from the /token endpoint
    mock_login_response = AsyncMock()
    mock_login_response.status_code = 200
    mock_login_response.json.return_value = {"access_token": "mock_internal_access_token", "token_type": "bearer"}
    mock_httpx_client.post.return_value = mock_login_response

    # Then, attempt to get a token with password grant type
    response = client.post(
        "/api/auth/token",
        data={
            "grant_type": "password",
            "username": "token@example.com",
            "password": "tokenpassword"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_for_access_token_authorization_code_grant(session, mock_httpx_client): 
    # Mock environment variables
    os.environ["CLIENT_ID"] = "test_client_id"
    os.environ["CLIENT_SECRET"] = "test_client_secret"
    os.environ["REDIRECT_URI"] = "http://localhost/test_callback"

    # Mock the external POST request 
    mock_external_token_response = AsyncMock()
    mock_external_token_response.status_code = 200
    mock_external_token_response.json.return_value = {"access_token": "mock_external_access_token", "token_type": "bearer"}
    mock_httpx_client.post.return_value = mock_external_token_response

    response = client.post(
        "/api/auth/token",
        data={
            "grant_type": "authorization_code",
            "code": "some_auth_code",  
            # Removed client_id, client_secret, redirect_uri from data payload
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["access_token"] == "mock_external_access_token"
    assert token_data["token_type"] == "bearer"

    # Clean up mock environment variables
    del os.environ["CLIENT_ID"]
    del os.environ["CLIENT_SECRET"]
    del os.environ["REDIRECT_URI"]
