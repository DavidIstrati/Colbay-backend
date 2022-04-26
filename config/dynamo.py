import boto3
from boto3.dynamodb.conditions import Key
import os
import json

ddb = boto3.client('dynamodb', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')

# ========================================================
# + GENERAL DYNAMODB FUNCTIONS
# ========================================================
#       - Dictionary with DynamoDB Schema
# ========================================================


dynamoTables = {
    'users': {'partitionKey': 'userId'},
    'listings': {'partitionKey': 'userId', 'sortKey': 'listingId'},
    'likes': {'partitionKey': 'userId', 'sortKey': 'listingId'},
}

IndexNames = {
    'listings': {
        'category-index': {'partitionKey': 'category'},
    },
}

# ========================================================
#       - Batch Get Item ( Get many items at once, constant complexity, get item by partition and sort key )
# ========================================================


def batchGetItemDDB(partitionKeys, sortKeys, TableName):
    partitionKeyName = dynamoTables[TableName]['partitionKey']
    sortKeyName = dynamoTables[TableName]['sortKey']

    keys = [{
        sortKeyName: {'S': sortKeys[index]},
        partitionKeyName: {'S': partitionKeys[index]}
    } for index in range(len(sortKeys))]

    items = ddb.batch_get_item(RequestItems={
        TableName: {'Keys': keys}
    })
    return items['Responses']


# ========================================================
#       - Get Item ( constant complexity, get item by partition and sort key )
# ========================================================


def getItemDDB(partitionKey, sortKey, TableName):
    try:
        if sortKey != None:
            partitionKeyName = dynamoTables[TableName]['partitionKey']
            sortKeyName = dynamoTables[TableName]['sortKey']
            Item = ddb.get_item(
                TableName=TableName,
                Key={partitionKeyName: {'S': partitionKey},
                    sortKeyName: {'S': sortKey}}
            )['Item']
            return True, Item
        else:
            partitionKeyName = dynamoTables[TableName]['partitionKey']
            Item = ddb.get_item(
                TableName=TableName,
                Key={partitionKeyName: {'S': partitionKey}}
            )['Item']
            return True, Item 
    except Exception as e:
        return False, [str(e), "python - dynamodb"]

# ========================================================
#       - Query ( O(nlogn) get a collection of items that match a pertition key )
# ========================================================


def queryDDB(partitionKey, TableName):
    try:
        partitionKeyName = dynamoTables[TableName]['partitionKey']
        return True, ddb.query(
            TableName=TableName,
            KeyConditionExpression=partitionKeyName + " = :part",
            ExpressionAttributeValues={
                ':part': {'S': partitionKey}
            }
        )['Items']
    except Exception as e:
        return False, [str(e), "python - dynamodb"]

# ========================================================
#       - Query Global Secondary Index with Filter
# ========================================================


def searchWithCategory(partitionKey, filterTerm, filterCol, IndexName, TableName):
    try:
        partitionKeyName = IndexNames[TableName][IndexName]['partitionKey']
        return True, ddb.query(
            TableName=TableName,
             IndexName=IndexName,
            KeyConditionExpression=partitionKeyName + " = :part",
            FilterExpression=f'begins_with({filterCol}, :sec)',
            ExpressionAttributeValues={
                ':part': {'S': partitionKey},
                ':sec': {'S': filterTerm}
            }
        )['Items']
    except Exception as e:
        return False, [str(e), "python - dynamodb"]

# ========================================================
#       - Batch Write Item ( write items to dynamo )
# ========================================================


def batchWriteDDB(Items, TableName):
    try:
        return True, ddb.batch_write_item(RequestItems={
            TableName: Items})
    except Exception as e:
        return False, [str(e), "python - dynamodb"]


# ========================================================
#       - Put Item ( write item to table )
# ========================================================


def putDDB(item, TableName):
    try:
        return True, ddb.put_item(
            TableName=TableName,
            Item=item
        )
    except Exception as e:
        return False, [str(e), "python - dynamodb"]

# ========================================================
#       - Update ( change current values of an item, if the item doesn't exist, it will create a new one )
# ========================================================


def updateDDB(partitionKey, sortKey, updateExpression, updateNames, updateParameters, TableName):
    try:
        if sortKey != None:
            partitionKeyName = dynamoTables[TableName]['partitionKey']
            sortKeyName = dynamoTables[TableName]['sortKey']
            return True, ddb.update_item(
                TableName=TableName,
                Key={partitionKeyName: {'S': partitionKey},
                    sortKeyName: {'S': sortKey}},
                UpdateExpression=updateExpression,
                ExpressionAttributeNames=updateNames,
                ExpressionAttributeValues=updateParameters,
                ReturnValues="UPDATED_NEW"
            )
        else:
            partitionKeyName = dynamoTables[TableName]['partitionKey']
            return True, ddb.update_item(
                TableName=TableName,
                Key={partitionKeyName: {'S': partitionKey}},
                UpdateExpression=updateExpression,
                ExpressionAttributeNames=updateNames,
                ExpressionAttributeValues=updateParameters,
                ReturnValues="UPDATED_NEW"
            )
    except Exception as e:
        return False, [str(e), "python - dynamodb"]


# ========================================================
#       - Delete ( delete current values of an item, if the item doesn't exist, it will create a new one )
# =======================================================

def deleteDDB(partitionKey, sortKey, TableName):
    try:
        partitionKeyName = dynamoTables[TableName]['partitionKey']
        sortKeyName = dynamoTables[TableName]['sortKey']
        return True, ddb.delete_item(TableName=TableName,
                                          Key={partitionKeyName: {'S': partitionKey},
                                               sortKeyName: {'S': sortKey}})
    except Exception as e:
        return False, [str(e), "python - dynamodb"]