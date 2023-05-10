from typing import Optional

from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import userControllers

from fastapi_jwt_auth import AuthJWT

@app.get("/user")
def GetUser(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp = userControllers(db).getUser(current_userId, None, None)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.get("/login")
def GetUser(email: str, password: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    code, resp = userControllers(db).getUser(None, email, password)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    access_token = Authorize.create_access_token(subject=resp.userId)
    return {"access_token": access_token}

@app.post("/user")
def PostUser(body: schemas.UserCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    code, resp =  userControllers(db).postUser(body)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    access_token = Authorize.create_access_token(subject=resp.userId)
    return {"access_token": access_token}

@app.post("/userVerificationCode")
def PostUserVerificationCode(verificationCode: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_userId = Authorize.get_jwt_subject()
    code, resp =  userControllers(db).postVerificationCode(verificationCode, current_userId)
    if(code != 200):
        raise HTTPException(status_code=code, detail=resp)
    return {"verified": True}