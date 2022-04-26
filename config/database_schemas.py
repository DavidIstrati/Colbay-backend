
from typing import List, Optional
from unicodedata import category

from pydantic import BaseModel

from .database_models import Listings, Likes

class LikeBase(BaseModel):
    userId: str
    listingId: str


class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    likeId: str

    class Config:
        orm_mode = True

class ListingBase(BaseModel):
    title: str = ""
    description: str = ""
    price: str
    image: str
    category: str = "other"
    keywords_list: List[str] = [""]
    date: Optional[str] = None
    likes: List[Like] = []


class ListingCreate(ListingBase):
    userId: str


class Listing(ListingCreate):
    listingId: str
    keywords: str
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
    date: str
    listings: List[Listing] = []
    likes: List[Like] = []

    class Config:
        orm_mode = True