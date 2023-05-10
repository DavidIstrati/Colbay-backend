from config import getUUID, models, s3, schemas, putItem
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from cleaning import StringStandardizer, ImgStandardizer, readImage

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

    def getListings(self, page: int, userId: str):
        items = self.db.query(models.Listings).filter(models.Listings.userId == userId).limit(page*20+1).offset((page-1)*20).all()
        if(items):
            return 200, items
        else:
            return 404, "No items found"

    def updateListing(self, updates: schemas.ListingUpdate, userId: str):
        parsedUpdates = {}
        for k, v in updates.dict().items():
            if (k != "listingId") and (v != None):
                parsedUpdates[k] = v
        item = self.db.query(models.Listings).filter(models.Listings.listingId == updates.listingId)
        tempItem = item.first()
        
        if not (tempItem.userId == userId):
            return 401, "Bad Authorization header."

        item.update(parsedUpdates)
        self.db.commit()
        item = item.first()
        if(item):
            return 200, item
        else:
            return 404, "No items found"

    async def updateMainImage(self, userId, listingId, image):
        mainImagePath = f'/{userId}/{listingId}/{getUUID()}.webp'
        pilImage = await readImage(image)
        imgWebp = ImgStandardizer(pilImage).downsizeImage().convertImage("RGB").imageToFormat("webp")
        resp, s3Item = putItem(mainImagePath, imgWebp)
        if resp != 'success':
            return 500, "Something went wrong"
        mainImagePath = f'https://d36q0hjddph8od.cloudfront.net/{mainImagePath}'
        item = self.db.query(models.Listings).filter(models.Listings.listingId == listingId)
        listingItem = item.first()
        if(not listingItem.published):
            item.update({"image": mainImagePath, "published": True})
        else:
            item.update({"image": mainImagePath})
        self.db.commit()
        item = item.first()
        if(item):
            return 200, item
        else:
            return 404, "No items found"
    
    async def updateSecondaryImage(self, userId, listingId, image):
        imagePath = f'/{userId}/{listingId}/{getUUID()}.webp'
        pilImage = await readImage(image)
        imgWebp = ImgStandardizer(pilImage).downsizeImage().convertImage("RGB").imageToFormat("webp")
        resp, s3Item = putItem(imagePath, imgWebp)
        if resp != 'success':
            return 500, "Something went wrong"
        imagePath = f'https://d36q0hjddph8od.cloudfront.net/{imagePath}'
        item = self.db.query(models.Listings).filter(models.Listings.listingId == listingId)
        listingItem = item.first()
        itemImages = listingItem.images
        if(itemImages):
            newImages = itemImages
            newImages.append(imagePath)
        else:
            newImages = [imagePath]
        if((not listingItem.published) and listingItem.image):
            item.update({"images": newImages, "published": True})
        else:
            item.update({"images": newImages})
        self.db.commit()
        item = item.first()
        if(item):
            return 200, item
        else:
            return 404, "No items found"


    def postListing(self, body, userId):
        listingId = getUUID()
            
        standardizedTitle = self.getStandardizedSearch(body.title)
        standardizedDescription = self.getStandardizedSearch(body.description)
        new_keywords_list = [self.getStandardizedSearch(value) for value in body.keywords.split(",")]
        keywords = ", ".join(new_keywords_list)

        likes = 0

        db_listing = models.Listings(userId=userId, listingId=listingId, title=body.title, category=body.category, standardizedTitle=standardizedTitle, standardizedDescription=standardizedDescription, keywords=keywords, description=body.description, price=body.price, images=[], keywords_list=new_keywords_list, published=False, date=None, likesCount=likes)

        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return 200, db_listing

    def searchListings(self,  term: Optional[str], category: Optional[str], priceStart: Optional[int] = None, priceEnd: Optional[int] = None, page: Optional[int] = 1):
        QueryObject = self.db.query(models.Listings).filter(models.Listings.published == True)
        if(category):
            QueryObject = QueryObject.filter(models.Listings.category == category)
        if(term):
            search = self.getStandardizedSearch(term)
            QueryObject = QueryObject.filter(models.Listings.searchTsVector.op('@@')(func.websearch_to_tsquery(search, postgresql_regconfig='english')))
        items = QueryObject.limit(page*20).offset((page-1)*20).all()
        if(items):
            return 200, items
        else:
            return 404, ""