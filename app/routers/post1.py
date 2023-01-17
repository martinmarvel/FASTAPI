
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.RestrictCreateResponsePost])
def getPosts(db: Session = Depends(get_db), skip:int=0, limit: int = 10, search:Optional[str]="" ):#fastapi de query parametrelerine örn:limit de olduğu gibi ulaşırız
    print(limit,skip)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RestrictCreateResponsePost)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db), currentUSer: int = Depends(oauth2.getCurrentUser)):

    newPost = models.Post(owner_id=currentUSer.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


@router.get("/{id}", response_model=schemas.RestrictCreateResponsePost)
def getPost(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id}: id li post bulunamadı")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), currentUSer: int = Depends(oauth2.getCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id}: id li post bulunamadı")

    if post.owner_id != currentUSer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perfom")

    postQuery.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RestrictCreateResponsePost)
def updatePost(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), currentUSer: int = Depends(oauth2.getCurrentUser)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id}: id li post bulunamadı")

    if post.owner_id != currentUSer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perfom")

    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()
