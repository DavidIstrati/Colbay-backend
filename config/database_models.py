from ast import Str
from unicodedata import category
from sqlalchemy import Boolean, Column, Computed, Index, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from .tsVector import TSVector

from .database_config import Base


class Users(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    graduationYear= Column(String)
    institution= Column(String)
    verifiedEmail= Column(Boolean)
    verificationCode = Column(Integer)
    date = Column(String)

    listings = relationship("Listings", back_populates="owner")
    likes = relationship("Likes", back_populates="owner")

class Listings(Base):
    __tablename__ = "listings"

    listingId = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    keywords_list = Column(ARRAY(String), nullable=False)
    keywords = Column(String, nullable=False)
    standardizedTitle = Column(String, nullable=False)
    standardizedDescription = Column(String, nullable=False)
    published = Column(Boolean, nullable=False)
    price = Column(String, nullable=False)
    image = Column(String)
    images = Column(ARRAY(String))
    userId = Column(String, ForeignKey("users.userId"), index=True, nullable=False)
    date = Column(String)
    likesCount = Column(Integer)

    searchTsVector = Column(TSVector(), Computed(
         """to_tsvector('english', "standardizedTitle" || ' ' || "standardizedDescription" || ' ' || "keywords" || ' ' || "category")""",
         persisted=True))

    __table_args__ = (Index('indexSearchTsVector',
          searchTsVector, postgresql_using='gin'),)

    owner = relationship("Users", back_populates="listings")
    likes = relationship("Likes", back_populates="listing")

class Likes(Base):
    __tablename__ = "likes"

    likeId = Column(String, primary_key=True, index=True)
    userId = Column(String, ForeignKey("users.userId"), index=True)
    listingId = Column(String, ForeignKey("listings.listingId"), index=True)
    date = Column(String)
    
    owner = relationship("Users", back_populates="likes")
    listing = relationship("Listings", back_populates="likes")

