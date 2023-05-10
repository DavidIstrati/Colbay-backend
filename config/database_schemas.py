
from typing import List, Optional
from unicodedata import category

from pydantic import BaseModel

from .database_models import Listings, Likes

import os

class Settings(BaseModel):
    authjwt_secret_key: str = os.environ['JWT_SECRET']

class LikeBase(BaseModel):
    listingId: str


class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    likeId: str
    userId: str

    class Config:
        orm_mode = True

class ListingBase(BaseModel):
    title: str = ""
    description: str = ""
    price: str
    category: str = "other"
    keywords: str
    date: Optional[str] = None
    likes: List[Like] = []


class ListingUpdate(BaseModel):
    listingId: str
    title: Optional[str]
    description: Optional[str]
    price: Optional[str]
    category: Optional[str]
    keywords: Optional[str]

class ListingCreate(ListingBase):
    pass


class Listing(ListingCreate):
    listingId: str
    keywords_list: str
    image: Optional[str]
    images: Optional[List[str]] = []
    published: bool = False
    likesCount: int
    standardizedTitle: str
    standardizedDescription: str


    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    firstName: str
    lastName: str
    graduationYear: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    userId: str
    institution: str
    verifiedEmail: bool
    verificationCode: int
    date: str
    listings: List[Listing] = []
    likes: List[Like] = []

    class Config:
        orm_mode = True