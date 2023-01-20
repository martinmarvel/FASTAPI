
from fastapi import FastAPI
from .routers import post1, user, auth, vote
#from . import models

from fastapi.middleware.cors import CORSMiddleware






#models.Base.metadata.create_all(bind=engine) alembic devreye girdiği için ihtiyacımız yok

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,#her istekden önce çalışan fonks.
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
