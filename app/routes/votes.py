from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schema, database, model, oauth2

from app.database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(model.Votes).filter(model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id)
    vote_found = vote_query.first()
    if(vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = model.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Vote added"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Vote removed"}