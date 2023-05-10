from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


from dotenv import load_dotenv

load_dotenv()

from .dynamo import *
from .dynamoParser import *
from .s3 import *
from .ses import *
from .uuid import getUUID

from sqlalchemy.orm import Session
from .database_config import SessionLocal, engine
import config.database_models as models 
import config.database_schemas as schemas 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return schemas.Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)