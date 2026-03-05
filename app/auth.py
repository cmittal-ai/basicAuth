from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from .models import UserInDB, Role, UserOut, UserCreate

SECRET_KEY = "yfugu238931y021fq#₹2₹42~K$₹%#$"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_fake_users_db: dict[str, UserInDB] = {}

def seed_users_once():
    if "viewer1" not in _fake_users_db:
        _fake_users_db["viewer1"] = UserInDB(
            username="viewer1",
            hashed_password=pwd_context.hash("viewerpass"),
            role="viewer",
        )
    if "admin1" not in _fake_users_db:
        _fake_users_db["admin1"] = UserInDB(
            username="admin1",
            hashed_password=pwd_context.hash("adminpass"),
            role="admin",
        )

seed_users_once()

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = _fake_users_db.get(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(payload: UserCreate) -> UserOut:
    username = payload.username.strip()

    if username in _fake_users_db:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = UserInDB(
        username=username,
        hashed_password=pwd_context.hash(payload.password),
        role=payload.role,
    )
    _fake_users_db[username] = user
    return UserOut(username=user.username, role=user.role)

def create_access_token(*, subject: str, role: Role, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    payload = decode_token(token)
    username = payload.get("sub")
    role = payload.get("role")
    if not username or role not in ("viewer", "admin"):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return UserOut(username=username, role=role)

def require_role(*allowed_roles: Role):
    def _dep(user: UserOut = Depends(get_current_user)) -> UserOut:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _dep