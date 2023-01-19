from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#pydentic model
class PostBase(BaseModel):
    title: str
    content: str
    
    # eğer kullanıcıdan published için boş gelirse default değeri "True" olacak
    published: bool = True
   



class PostCreate(PostBase):
    pass

class RestrictedUserOut(BaseModel):#restricted dedik aslında classın adı Post fakat schemeaları kullanırken hangi datayı gösterip göstermyeceğimizi seçebiliriz

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class RestrictCreateResponsePost(PostBase):#örn olarak bırakıldı geriye dönmesini istemediğimiz dataları silebilirz
    id: int
    owner_id: str
    created_at: datetime
    owner:RestrictedUserOut#models.py daki owner ile alakalı
    
    #pydantic  sadece dict kabul etttiği için vt nında geriye dönen cevap sqlalchemy modeli tanımaz, tanıması için aşşağıdaki config yapılır
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: RestrictCreateResponsePost
    Votes: int
    
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr #email için özel email string türünde pydantic kütüphanesinden geldi
    password: str




    
class UserLogin(BaseModel):
        email: EmailStr
        password: str


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)#conint directorynin 0 ya da bir olup olmadığını kontrol etmeye yarıyor "le" less than equal

