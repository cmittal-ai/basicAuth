# FastAPI Auth API (JWT + Roles)

This project is a simple FastAPI service that supports:
- User **signup** (stored in-memory)
- **Login** using OAuth2 password flow
- **JWT** access tokens
- **Role-based access control** (`viewer`, `admin`)

> Note: Users are stored in-memory (a Python dict/array). Data will reset when the server restarts.

---

## Prerequisites
- Python 3.9.x

---

## Setup

### 1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate

### 2) Install dependencies
```bash
Copy code
pip install -r requirements.txt

### 3) Run the server
```bash
Copy code
python -m uvicorn app.main:app --reload
Swagger UI:

http://127.0.0.1:8000/docs
API Endpoints
POST /auth/signup
Creates a new user in the in-memory store.

Example:

```bash
Copy code
curl -X POST "http://127.0.0.1:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"username":"newviewer","password":"secret123","role":"viewer"}'
POST /auth/login
Logs in a user and returns a JWT access token.

Example:

```bash
Copy code
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=newviewer&password=secret123"
Response:

json
Copy code
{
  "access_token": "<TOKEN>",
  "token_type": "bearer"
}
Authorization (Bearer Token)
For protected endpoints, pass the token in the request header:

Authorization: Bearer <TOKEN>

Protected Endpoints
GET /me
Returns the logged-in user details.

```bash
Copy code
curl "http://127.0.0.1:8000/me" \
  -H "Authorization: Bearer <TOKEN>"
GET /reports (viewer/admin)
```bash
Copy code
curl "http://127.0.0.1:8000/reports" \
  -H "Authorization: Bearer <TOKEN>"
POST /admin/users (admin only)
```bash
Copy code
curl -X POST "http://127.0.0.1:8000/admin/users" \
  -H "Authorization: Bearer <TOKEN>"
