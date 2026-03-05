# FastAPI Auth API (JWT + Roles)

A small FastAPI project that provides:
- User signup (in-memory store)
- Login with OAuth2 password flow
- JWT-based authentication
- Role-based authorization (`viewer`, `admin`)

> Note: Users are stored in-memory (a dict/array in code). Data resets whenever the server restarts.

## Prerequisites
- Python 3.9.x

## Setup

### 1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate