from typing import Optional
from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import likeControllers
import time

from fastapi_jwt_auth import AuthJWT

@app.get("/like")
def GetLike(likeId: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    code, resp = likeControllers(db).getLike(likeId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.delete("/like")
def DeleteLike(likeId: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp = likeControllers(db).deleteLike(likeId, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/like")
def PostLike(body: schemas.LikeCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  likeControllers(db).postLike(body, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp


@app.get("/likes")
def GetLikes(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp = likeControllers(db).getLikes(current_userId)
    time.sleep(1)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp