import boto3
import os

boto3.resource('dynamodb', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')

# To go from low-level format to python
def parse_dynamo_item(item):
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    return {k: deserializer.deserialize(v) for k,v in item.items()}

# To go from python to low-level format
def dict_to_item(item):
    serializer = boto3.dynamodb.types.TypeSerializer()
    return {k: serializer.serialize(v) for k,v in item.items()}