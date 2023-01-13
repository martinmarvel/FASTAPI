
from fastapi import FastAPI, Response, status, HTTPException
# post kısmında body ile, post işleminden geriye dönen datayı almış oluruz payload da saklanan datayı kullanabiliriz
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

# BaseModel ile api şeması yani datanın bize bize nasıl ulaştırılacağını belirleriz


class Post(BaseModel):
    title: str
    content: str
    # eğer kullanıcıdan published için boş gelirse default değeri "True" olacak
    published: bool = True
    rating: Optional[int] = None




myPosts = [{"title": "title1", "content": "conten1", "id": 1}, {"title": "title12", "content": "conten12", "id": 2},
           {"title": "title13", "content": "conten13", "id": 3}]
# fast api instance ı oluışturduk
# uvicorn main:app --reload virtual server başlttık fast api özelliği


def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


def findIndexPostFor(id):
    for i, p in enumerate(myPosts):
        if p['id'] == id:
            return i


@app.get("/")  # burakadi "@" bir dekaratör, altında yazılan kodu fastapi ile ilişkilendirmeye yarar, "get" http metodu, "/" root path denir,
# path değişebilir örneğin "/login" url de login path inde işlemler yapmamıza yarar
async def root():  # fonks. ismi önemli değil
    # buradaki data jsona dönüştürülüyor
    return {"message": "Hello Ömer1 World"}


@app.get("/posts")
def getPosts():
    return {"sent data": myPosts}


# post requestinin kodunu 201 yaptık,burası yokken 200 OK idi
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(newPost: Post):
    print(newPost)
    # newPost pydentic kütüphansi şeklinde gelir, onu dict() ile python a uygun hale getiririz
    print(newPost.dict())
    postDict = newPost.dict()
    postDict["id"] = randrange(0, 1000000)
    myPosts.append(postDict)
    return {"data": postDict}


@app.get("/posts/{id}")
# response kullanımı kaldırıldı, kullanıldığı biçimi aşşağıda yorum satırı olarak duruyor
def getPost(id: int, response: Response):

    post = findPost(id)
    if not post:  # eğer post bulunamazsa çalışacak olan 404 kodu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id}: id li post bulunamadı")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return{"id bulunamadı": id }
    return {"post bilgisi": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):


    index1 = findIndexPostFor(id)

    if index1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id}: id li post bulunamadı")

    myPosts.pop(index1)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
def updatePost(id: int, post:Post):
    index1 = findIndexPostFor(id)

    if index1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id}: id li post bulunamadı")

    postDict = post.dict()
    postDict["id"] = id
    myPosts[index1] = postDict
    return {"mesaj":postDict}
print()