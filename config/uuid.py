import uuid
import base64

def getUUID():
    # Note that uuid1() may compromise privacy since it creates a UUID containing the computer’s network address. uuid4() creates a random UUID.
    return str(base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8'))