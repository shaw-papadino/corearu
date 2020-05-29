from fastapi import Depends
from sqlalchemy.orm import Session
from controller.db_create import SessionLocal
from controller.User import User
import controller.UserIn as userin

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

def get_user(user_id: str, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def create_user(user_id: str, db: Session):
    user = User(id = user_id)
    db.add(user)
    db.commit()
    user = get_user(user_id, db)
    return user

def update_user(user_id: str, user_book: str, user_status, db: Session):
    user = get_user(user_id, db)
    user.book = user_book
    user.is_status = user_status
    db.commit()
    user = get_user(user_id,db)
    return user
