# Specification: Better-Auth Integration

## 1. Objective

To implement a user authentication system (Signup and Signin) using the `better-auth` library. The system must capture user background information at signup to enable future content personalization. This replaces the previous Python-native authentication system.

## 2. Architecture

The implementation introduces a two-service backend architecture to accommodate the Node.js-based `better-auth` library alongside the main Python-based FastAPI application.

### 2.1. FastAPI Service (Main Backend)

- **Framework:** Python, FastAPI
- **Port:** `8000`
- **Responsibilities:** Continues to serve all non-authentication-related APIs, such as the `/api/chatbot` endpoint.
- **Auth Role:** This service is no longer responsible for user authentication. The routes in `app/api/auth.py` are now unused by the frontend.

### 2.2. Better-Auth Service (Authentication Backend)

- **Framework:** Node.js, Express, TypeScript
- **Port:** `8001`
- **Location:** `fastapi-backend/auth_server.ts`
- **Responsibilities:** Exclusively handles user signup and login.
- **Core Logic:** Uses the `better-auth` library to manage user accounts, sessions, and database interactions with the Neon PostgreSQL database.

### 2.3. Frontend (Docusaurus)

- The React-based frontend now communicates with two different backend services:
  - The **Better-Auth Service** (`http://localhost:8001`) for `/signup` and `/login` requests.
  - The **FastAPI Service** (`http://localhost:8000`) for all other API requests (e.g., chatbot).

## 3. API Endpoints (Better-Auth Service)

The `auth_server.ts` Express server exposes the following endpoints:

### `POST /signup`

- **Description:** Registers a new user.
- **Request Body:** `application/json`
  ```json
  {
    "email": "user@example.com",
    "password": "user_password",
    "softwareBackground": "e.g., Python, C++",
    "hardwareBackground": "e.g., Robotics, Arduino"
  }
  ```
- **Response:** A user object, as defined by `better-auth`.

### `POST /login`

- **Description:** Authenticates a user and starts a session.
- **Request Body:** `application/json`
  ```json
  {
    "email": "user@example.com",
    "password": "user_password"
  }
  ```
- **Response:** A session object, as defined by `better-auth`. The frontend stores this in `localStorage`.

## 4. Data Model

The user data is stored in the Neon PostgreSQL database, managed by `better-auth`. The schema includes the following fields:

- `email`: User's email address (primary identifier).
- `password`: Hashed password.
- `softwareBackground`: A string describing the user's software experience.
- `hardwareBackground`: A string describing the user's hardware experience.

## 5. Frontend Components

The following files were modified to integrate with the new authentication service:

- **`docusaurus-book/src/utils/api.js`**: Auth-related URLs were updated to point to the new service on port `8001`.
- **`docusaurus-book/src/pages/signup.js`**: The signup form was updated to use the new endpoint and send a `application/json` payload with the correct field names.
- **`docusaurus-book/src/pages/login.js`**: The login form was updated to use the new endpoint, send a `application/json` payload, and handle the session object returned by `better-auth`.

## 6. Running the System

To run the complete application, two backend services must be running in separate terminals.

1.  **FastAPI Service:**
    -   Navigate to `fastapi-backend/`
    -   Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
2.  **Better-Auth Service:**
    -   Navigate to `fastapi-backend/`
    -   Run: `npm start`
