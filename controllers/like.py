from config import getUUID, models, schemas
from typing import Optional, List
from sqlalchemy.orm import Session


class likeControllers():
    def __init__(self, db: Session):
        self.db = db

    def getLike(self, likeId: str):
        item = self.db.query(models.Likes).filter(models.Likes.likeId == likeId).first()
        if(item):
            return 200, item
        else:
            return 404, "No items found"

    def deleteLike(self, likeId: str, userId: str):
        item = self.db.query(models.Likes).filter(models.Likes.likeId == likeId)
        tempItem = item.delete()
        if not (tempItem.userId == userId):
            return 401, "Bad Authorization header."
        self.db.commit()
        if(item):
            return 200, item
        else:
            return 404, "No items found"

    def getLikes(self, userId: Optional[str], listingId: Optional[str] = None):
        if(userId):
            items = self.db.query(models.Likes, models.Listings).filter(models.Likes.userId == userId).filter(models.Listings.listingId == models.Likes.listingId).limit(20).all()
        elif(listingId):
            items = self.db.query(models.Likes, models.Users).filter(models.Likes.listingId == listingId).filter(models.Users.userId == models.Likes.userId).limit(20).all()
        else:
            return 500, "internal server error, please contact us"
        if(items):
            return 200, items
        else:
            return 404, "No items found"

    def postLike(self, like: schemas.LikeCreate, userId: str):
        likeId = userId + like.listingId

        db_like = models.Likes(userId=userId, listingId=like.listingId, likeId=likeId)
        
        self.db.add(db_like)
        self.db.commit()
        self.db.refresh(db_like)
        return 200, db_like
