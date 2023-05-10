from typing import List, Optional, Union

from fastapi import File, Form, UploadFile
from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import listingControllers
from sqlalchemy.orm import Session
import time 

from fastapi_jwt_auth import AuthJWT

@app.get("/listing")
def GetListing(listingId: str, db: Session = Depends(get_db)):
    code, resp = listingControllers(db).getListing(listingId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/listing")
def PostListing(body: schemas.ListingCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  listingControllers(db).postListing(body, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.patch("/listingMainImage")
async def PatchMainImageListing(listingId: str  = Form(default=""), image: UploadFile = File(default=None),  Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  await listingControllers(db).updateMainImage(current_userId, listingId, image)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.patch("/listingSecondaryImage")
async def PatchSecondaryImageListing(listingId: str  = Form(default=""), image: UploadFile = File(default=None), Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  await listingControllers(db).updateSecondaryImage(current_userId, listingId, image)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.patch("/listing")
def PatchListing(body: schemas.ListingUpdate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  listingControllers(db).updateListing(body, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp


@app.get("/listings")
def GetListings(page: int = 1, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp = listingControllers(db).getListings(page, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.get("/searchListings")
def SearchListings(term: Optional[str] = None, category: Optional[str] = None, priceStart: Optional[int] = None, priceEnd: Optional[int] = None, db: Session = Depends(get_db)):
    code, resp = listingControllers(db).searchListings(term, category, priceStart, priceEnd)
    time.sleep(2)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp