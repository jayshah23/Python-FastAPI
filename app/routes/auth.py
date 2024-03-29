from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import utils
from sqlalchemy.orm import Session

from .. import database, schema, model, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User {user_credentials.username} not found")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password")

    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}