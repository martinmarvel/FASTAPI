
from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
#from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
#from typing import List, Optional

router = APIRouter()






@router.get("/posts", response_model = List[schemas.RestrictCreateResponsePost])
#List import edildi geriye dönen postları listeye almış olduk
def getPosts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# post requestinin kodunu 201 yaptık,burası yokken 200 OK idi
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.RestrictCreateResponsePost)
# buradaki response model,create sorgusu sonucunda
#geriye dönecek attribute/data nın şemesını belirlemeye yarıyor. yani yeni post bütün olarak gider fakat geriye dönen response da sadece
#belirlenen alanlar bulunur
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db)):

    ##Yorum satırına alınan kod ORM kullanmadan önce createPost un çalışır halidir
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
    #(newPost.title, newPost.content, newPost.published))

    #newPost = cursor.fetchone()
    #conn.commit()# ekleme yaptıktan sonra commit ile kaydetmiş oluruz

    newPost = models.Post(**post.dict())#models.py içinde post şemasından geldi **post.dict ise gelen attributelerin hepsini almaya yaradı
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost

""" print(newPost)
    # newPost pydentic kütüphansi şeklinde gelir, onu dict() ile python a uygun hale getiririz
    print(newPost.dict())
    postDict = newPost.dict()
    postDict["id"] = randrange(0, 1000000)
    myPosts.append(postDict)
    return {"data": postDict}
    """


@router.get("/posts/{id}", response_model=schemas.RestrictCreateResponsePost)
# response kullanımı kaldırıldı, kullanıldığı biçimi aşşağıda yorum satırı olarak duruyor
def getPost(id: int, db: Session = Depends(get_db)):
    ##Yorum satırına alınan kod ORM kullanmadan önce createPost un çalışır halidir
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post=cursor.fetchone()
    #print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    

    if not post:  # eğer post bulunamazsa çalışacak olan 404 kodu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id}: id li post bulunamadı")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return{"id bulunamadı": id }
    return post

  #post = findPost(id) getPost() api sinde vt nına bağlanmadan önce dummy vt(myPosts) ta id ile yakalama için kullanıldı

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING*""", (str(id),))
    
    #eletedPost=cursor.fetchone()
    #conn.commit()


    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id}: id li post bulunamadı")

    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#   deletedPost = findIndexPostFor(id) deletePost() api sinde vt nına bağlanmadan önce dummy vt(myPosts) ta id ile yakalama için kullanıldı



@router.put("/posts/{id}", response_model=schemas.RestrictCreateResponsePost)
def updatePost(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)

    post = postQuery.first()#yukarıdaki query ile özel id li post sorguland, bu satır ile de sorgulanan ilk post yaklandı.

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*""", 
    #(post.title, post.content, post.published, str(id)))
    #updatedPost=cursor.fetchone()
    #conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id}: id li post bulunamadı")

    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()

    
"""index1 = findIndexPostFor(id) updatePost() api sinde vt nına bağlanmadan önce dummy vt(myPosts) ta id ile yakalama için kullanıldı
postDict = post.dict()
    postDict["id"] = id
    myPosts[index1] = postDict"""

