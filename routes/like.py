from typing import Optional
from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import likeControllers

@app.get("/like")
def GetLike(likeId: str, db: Session = Depends(get_db)):
    code, resp = likeControllers(db).getLike(likeId)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp

@app.delete("/like")
def DeleteLike(likeId: str, db: Session = Depends(get_db)):
    code, resp = likeControllers(db).deleteLike(likeId)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/like")
def PostLike(body: schemas.LikeCreate, db: Session = Depends(get_db)):
    code, resp =  likeControllers(db).postLike(body)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp


@app.get("/likes")
def GetLikes(userId: Optional[str] = None, listingId: Optional[str] = None, db: Session = Depends(get_db)):
    code, resp = likeControllers(db).getLikes(userId, listingId)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp