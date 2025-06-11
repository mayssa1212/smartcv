from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import UserCreate, UserOut
from app.crud import create_user, get_user, get_users
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db=db, user=user)

@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Récupère les informations de l'utilisateur actuellement connecté."""
    return current_user
