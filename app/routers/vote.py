from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), currentUser: int = Depends(oauth2.getCurrentUser)):

    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post {vote.post_id} you voted does not exist")
    

    
    voteQuery=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == currentUser.id)# "vote dan gelen idsi uyan vote var mı kontrol
    
    foundVote = voteQuery.first()
    
    if (vote.dir==1):#schema dan gelen dir
        if foundVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{currentUser.id} already voted on {vote.post_id}")
        
        newVote = models.Vote(post_id = vote.post_id, user_id= currentUser.id)
        db.add(newVote)
        db.commit()
        return {"message":"vote added"}
    else:
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not exist")

        voteQuery.delete(synchronize_session=False)
       
        db.commit()

        return {"message":"vote deleted"}