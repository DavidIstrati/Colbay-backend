from config import app
from routes import *

@app.get("/")
def root():
    return {"Hello": "World"}

