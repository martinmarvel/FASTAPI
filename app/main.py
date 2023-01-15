
from fastapi import FastAPI
#from fastapi import FastAPI, Response, status, HTTPException, Depends
# post kısmında body ile, post işleminden geriye dönen datayı almış oluruz payload da saklanan datayı kullanabiliriz
#from fastapi.params import Body
#from pydantic import BaseModel
#from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .routers import post1, user


from . import models
#from . import models, schemas, utils
from .database import engine

#from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)



app = FastAPI()


app.include_router(post1.router)

app.include_router(user.router)

@app.get('/')  
async def root(): 
    return {"message": "Hello Ömer1 World"}

#postgre vt nına bağlanma kodu
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='258369', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("vt bağlantı başarılı")
        break
    except Exception as error:
        print("vt bağlantısı başarılı olamadı")
        time.sleep(10)



"""myPosts = [{"title": "title1", "content": "conten1", "id": 1}, {"title": "title12", "content": "conten12", "id": 2},
           {"title": "title13", "content": "conten13", "id": 3}]



def findPost(id):
    for p in posts:
        print
        if p["id"] == id:
            return p


def findIndexPostFor(id):
    for i, p in enumerate(myPosts):
        if p['id'] == id:
            return i
"""














