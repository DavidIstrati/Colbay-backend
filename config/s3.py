import boto3
from io import StringIO, BytesIO

client = boto3.client('s3')

def putItem(filepath, body, bucketName='colbayuserbucket'):
   try:
      return "success", client.put_object(Body=body, Bucket=bucketName, Key=filepath)
   except:
      return "failed", "failed putItem in S3" 

def getItem(filepath, bucketName='colbayuserbucket'):
   try:
      return "success", client.get_object(Bucket=bucketName, Key=filepath)["Body"].read().decode("UTF-8")
   except:
      return "failed", "failed getItem in S3"

def deleteItem(filepath, bucketName):
    return ''