from unicodedata import category
from config import getUUID, models, schemas
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from cleaning import StringStandardizer

class listingControllers():
    def __init__(self, db: Session):
        self.db = db

    def getStandardizedSearch(self, value: str) -> str:
        return  StringStandardizer(value).removeSpecialCharacters().removeWhitespace().lowercase().trim().getValue()

    def getListing(self, listingId: str):
        item = self.db.query(models.Listings).filter(models.Listings.listingId == listingId).first()
        if(item):
            return 200, item
        else:
            return 404, "No items found"

    def getListings(self, userId: str):
        items = self.db.query(models.Listings).filter(models.Listings.userId == userId).limit(20).all()
        if(items):
            return 200, items
        else:
            return 404, "No items found"

    def postListing(self, listing: schemas.ListingCreate):
        listingId = getUUID()
            
        standardizedTitle = self.getStandardizedSearch(listing.title)
        standardizedDescription = self.getStandardizedSearch(listing.description)
        keywords_list = [self.getStandardizedSearch(value) for value in listing.keywords_list]
        keywords = ", ".join(keywords_list)
        
        likes = 0

        db_listing = models.Listings(userId=listing.userId, listingId=listingId, title=listing.title, category=listing.category, standardizedTitle=standardizedTitle, standardizedDescription=standardizedDescription, keywords=keywords, description=listing.description, price=listing.price, image=listing.image, keywords_list=listing.keywords_list, date=listing.date, likesCount=likes)

        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return 200, db_listing

    def searchListings(self,  term: Optional[str], category: Optional[str], keywords: Optional[str], startDate: Optional[int], endDate: Optional[int], date: Optional[int], priceStart: Optional[int], priceEnd: Optional[int], likesMin: Optional[int]):
        if(category):
            if(term):
                search = self.getStandardizedSearch(term)
                items = self.db.query(models.Listings).filter(models.Listings.category == category).filter(models.Listings.searchTsVector.op('@@')(func.websearch_to_tsquery(search, postgresql_regconfig='english'))).limit(20).all()
            else:
                items = self.db.query(models.Listings).filter(models.Listings.category == category).limit(20).all()
            if(items):
                return 200, items
            else:
                return 400, "No items found"
        elif(term):
            search = self.getStandardizedSearch(term)
            items = self.db.query(models.Listings).filter(models.Listings.searchTsVector.op('@@')(func.websearch_to_tsquery(search, postgresql_regconfig='english'))).limit(20).all()
            if(items):
                return 200, items
            else:
                return 400, "No items found"
        else:
            return 500, ""