from fastapi import APIRouter, Depends, HTTPException
from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer
from auth.admin import validate_admin
from pydantic import BaseModel

router = APIRouter()

# Mock user database
users = [{"id": 1, "email": "user@example.com", "name": "John Doe"}]



# Define a Pydantic model for the request body
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(login_request: LoginRequest):
    email = login_request.email
    password = login_request.password

    if validate_admin(email, password):
        return {"access_token": signJWT(email)}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/users", dependencies=[Depends(JWTBearer())])
def get_users():
    return users
