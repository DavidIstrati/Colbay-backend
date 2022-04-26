from typing import Optional
from config import app, HTTPException, Session, Depends, get_db, schemas
from controllers import userControllers

@app.get("/user")
def GetUser(userId: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, db: Session = Depends(get_db)):
    code, resp = userControllers(db).getUser(userId, email, password)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/user")
def PostUser(body: schemas.UserCreate, db: Session = Depends(get_db)):
    code, resp =  userControllers(db).postUser(body)
    if(code != 200):
        return HTTPException(status_code=code, detail=resp)
    return resp