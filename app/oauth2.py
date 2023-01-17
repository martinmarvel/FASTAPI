from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import Depends ,status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from.config import settings

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret key
#algoritm
#expretayion time


#access token function
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCSESS_TOKEN_EXPIRE_MINUTES

def createAccsessToken(data: dict):
    toEncode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp":expire})
    

    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJwt


#verify token faunction

def verifyAccsessToken(token: str, credentialsException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM)

        id: str = payload.get("userId")
 
        if id is None:
            raise credentialsException
        tokenData = schemas.TokenData(id=id)
    except JWTError:
        raise credentialsException

    return tokenData



def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(database.get_db)):
    credentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token=verifyAccsessToken(token, credentialsException)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user