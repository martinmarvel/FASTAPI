from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RestrictedUserOut)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword

    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


@router.get("/{id}", response_model=schemas.RestrictedUserOut)
def getUSer(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} : li kullanıcı bulunamadı")

    return user
