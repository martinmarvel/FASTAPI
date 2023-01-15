from pydantic import BaseModel, EmailStr
from datetime import datetime

#pydentic model
class PostBase(BaseModel):
    title: str
    content: str
    # eğer kullanıcıdan published için boş gelirse default değeri "True" olacak
    published: bool = True
   
class PostCreate(PostBase):
    pass

class RestrictCreateResponsePost(PostBase):#örn olarak bırakıldı geriye dönmesini istemediğimiz dataları silebilirz
    id: int
    created_at: datetime
    #pydantic  sadece dict kabul etttiği için vt nında geriye dönen cevap sqlalchemy modeli tanımaz, tanıması için aşşağıdaki config yapılır
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr #email için özel email string türünde pydantic kütüphanesinden geldi
    password: str

class RestrictedUserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



