from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import model, schema, utils
from ..database import get_db

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=schema.UserResponse)
def createUser(user: schema.User, db: Session = Depends(get_db)):
    user.password = utils.get_password_hash(user.password)
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/{id}", response_model=schema.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return user
