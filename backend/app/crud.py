from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import UserCreate
from app.security import get_password_hash  # Importez la fonction de hachage

def get_user(db: Session, user_id: int = None, email: str = None):
    if user_id:
        return db.query(UserModel).filter(UserModel.id == user_id).first()
    elif email:
        return db.query(UserModel).filter(UserModel.email == email).first()
    return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Utilisez la fonction de hachage pour sécuriser le mot de passe
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
