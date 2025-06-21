from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate
from app.services import user
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=User)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = user.get_user_by_email(db, email=user_data.email) 
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.create_user(db, user_data)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = user.update_user(db, user_id, user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}