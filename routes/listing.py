from typing import Optional
from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import listingControllers
from sqlalchemy.orm import Session

@app.get("/listing")
def GetListing(listingId: str, db: Session = Depends(get_db)):
    code, resp = listingControllers(db).getListing(listingId)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/listing")
def PostListing(body: schemas.ListingCreate, db: Session = Depends(get_db)):
    code, resp =  listingControllers(db).postListing(body)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp


@app.get("/listings")
def GetListings(userId: str, db: Session = Depends(get_db)):
    code, resp = listingControllers(db).getListings(userId)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp

@app.get("/searchListings")
def SearchListings(term: Optional[str] = None, category: Optional[str] = None, keywords: Optional[str] = None, startDate: Optional[int] = None, endDate: Optional[int] = None, date: Optional[int] = None, priceStart: Optional[int] = None, priceEnd: Optional[int] = None, likesMin: Optional[int] = None, db: Session = Depends(get_db)):
    code, resp = listingControllers(db).searchListings(term, category, keywords, startDate, endDate, date, priceStart, priceEnd, likesMin)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp