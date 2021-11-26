from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from .. import model, schema, oauth2
from ..database import get_db

router = APIRouter(prefix="/post", tags=["Post"])

# @router.get("/", response_model=List[schema.PostResponse])
@router.get("/", response_model=List[schema.PostWithVote])
def getPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(model.Post).filter(model.Post.user_id == current_user.id).all()
    # posts = db.query(model.Post).filter(model.Post.user_id == current_user.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(model.Post, func.count(model.Votes.post_id).label("votes")).join(model.Votes, model.Votes.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/")
def createPost(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = model.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Message": "Post created successfully", "Post": new_post}

# @router.get("/{id}", response_model=schema.PostResponse)
@router.get("/{id}", response_model=schema.PostWithVote)
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    post = db.query(model.Post, func.count(model.Votes.post_id).label("votes")).join(model.Votes, model.Votes.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@router.put("/{id}")
def updatePost(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(model.Post).filter(model.Post.id == id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if posts.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to perform requested action")
    posts.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"Message": "Post updated successfully"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePOst(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(model.Post).filter(model.Post.id == id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if posts.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not allowed to perform requested action")
    posts.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Post deleted"}