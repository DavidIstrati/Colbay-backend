from typing import Union
from PIL import Image
import io

from fastapi import UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

class ImgStandardizer():
    def __init__(self, image):
        self.image = image
        
    def imageToFormat(self, format:str="webp"):
        newImg = io.BytesIO()
        self.image.save(newImg, format=format)
        return newImg.getvalue()
        
    def downsizeImage(self):
        width, height = self.image.size
        if((width >= 1620) and (height>1080)):
            newsize = (1620, 1080)
            newImg = self.image.resize(newsize)
            return ImgStandardizer(newImg)
        return ImgStandardizer(self.image)

    def convertImage(self, format):
        newImg = self.image.convert(format)
        return ImgStandardizer(newImg)

async def readImage(image: StarletteUploadFile):
    pilImage = await image.read()
    return Image.open(io.BytesIO(pilImage))
