
from fastapi import FastAPI
from .routers import post1, user, auth, vote
from . import models
from .database import engine






models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post1.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)


@app.get('/')
async def root():
    return {"message": "Hello Ömer1 World"}


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
