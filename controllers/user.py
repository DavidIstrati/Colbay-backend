from sqlalchemy.orm import Session
from config import getUUID, models, schemas

import base64
from typing import Optional
import hashlib
import os
import re

emailValidator = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
# Define a function for
# for validating an Email
 
 
def check(email: str) -> bool:
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(emailValidator, email)):
        return True
 
    else:
        return False

def getHashed(text: str) -> str:
    return hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        text.encode('utf-8'), # Convert the password to bytes
        os.environ["salt"].encode('utf-8'), # Provide the salt
        124790 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

def getUserId(email: str)-> str:
    return base64.urlsafe_b64encode(getHashed(email)).decode()

class userControllers():
    def __init__(self, db: Session):
        self.db = db
    def getUser(self, userId: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        if((email != None) and (password!=None)):
            item = self.db.query(models.Users).filter(models.Users.email == email).first()
            if(item):               
                hashedPassword = getHashed(password)
                if(hashedPassword == item.password):
                    return 200, item
                else:
                    return 400, "Email or password are wrong"

            else:
                return 404, "There is no account with this email adress"
        elif(userId != None):
            item = self.db.query(models.Users).filter(models.Users.userId == userId).first()
            if(item):
                return 200, item
            else:
                return 404, "There is no account with this id"
        else:
            return 500, "Internal server error - please contact us"
    def postUser(self, body: schemas.UserCreate):
        email = body.email
        password = body.password
        firstName = body.firstName
        lastName = body.lastName
        graduationYear = body.graduationYear
        
        if(not check(email)):
            return 422, "Email is not valid"

        item = self.db.query(models.Users).filter(models.Users.email == email).first()

        if(item):            
            if(item.verifiedEmail):
                return 409, "An account with this email already exists"
            else:
                self.db.query(models.Users).filter(models.Users.email == email).delete()

        hashedPassword = getHashed(password)
        hashedEmail = getUserId(email)

        institution = re.findall("(?<=@)[^.]*.[^.]*(?=\.)", email) # get domain without tld

        db_user = models.Users(userId=hashedEmail, email=email, firstName=firstName, lastName=lastName, password=hashedPassword, graduationYear=graduationYear, institution=institution, verifiedEmail=False)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return 200, db_user