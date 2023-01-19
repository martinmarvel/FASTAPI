
from fastapi import APIRouter,Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from .. import database, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login') #response_model=schemas.Token
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
   

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #create token
    accsessToken = oauth2.createAccsessToken(data={"userId":user.id})

    #return token
    return {"accsessToken":accsessToken, "tokenType":"Bearer"}