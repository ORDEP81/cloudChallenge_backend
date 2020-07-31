import boto3
import json
import os


# create the client outside of the handler
DEFAULT_REGION = "us-east-1"
region_name = os.environ[DEFAULT_REGION]
dynamo = boto3.client('dynamodb')
table_name = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    response = dynamo.update_item(
        TableName= table_name,
        Key = {
            "id" : {'S' : 'counter'}
        },
        UpdateExpression = 'ADD visitor :inc',
        ExpressionAttributeValues = {
            ':inc': {'N':'1'}
        },
        ReturnValues="UPDATED_NEW"
    )
    
    dbresponse = json.dumps(int(response["Attributes"]["visitor"]["N"]))
    
    corsresponse = {
        'statusCode': 200,
        'body' : dbresponse,
        'headers': {
          "Content-Type" : "application/json",
          "Access-Control-Allow-Origin" : "",
          "Allow" : "GET, OPTIONS, POST",
          "Access-Control-Allow-Methods" : "GET, OPTIONS, POST",
          "Access-Control-Allow-Headers" : ""
        },
    }
    return corsresponse    
    