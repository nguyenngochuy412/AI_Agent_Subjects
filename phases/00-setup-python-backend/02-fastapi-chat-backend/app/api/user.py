from fastapi import APIRouter
from pydantic import BaseModel

class UserOut(BaseModel):
    name: str

router = APIRouter(tags=["user_out"])

@router.get("/user", response_model=UserOut)
def get_user():
    return {"name": "An", "password_hash": "abc123"}