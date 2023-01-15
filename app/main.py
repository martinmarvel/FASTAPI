
from fastapi import FastAPI, Response, status, HTTPException
# post kısmında body ile, post işleminden geriye dönen datayı almış oluruz payload da saklanan datayı kullanabiliriz
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()



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
















