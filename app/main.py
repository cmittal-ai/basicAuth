from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .auth import authenticate_user, create_access_token, require_role, get_current_user, create_user
from .models import Token, UserOut, UserCreate

app = FastAPI(title="Login API with Roles")

@app.post("/auth/signup", response_model=UserOut, status_code=201)
def signup(payload: UserCreate):
    return create_user(payload)

@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(subject=user.username, role=user.role)
    return Token(access_token=token)

@app.get("/me", response_model=UserOut)
def me(user: UserOut = Depends(get_current_user)):
    return user

@app.get("/reports")
def view_reports(user: UserOut = Depends(require_role("viewer", "admin"))):
    return {"message": f"Hello {user.username}, you can view reports."}

@app.post("/admin/users")
def admin_create_user(user: UserOut = Depends(require_role("admin"))):
    return {"message": f"Hello {user.username}, you can perform admin actions."}