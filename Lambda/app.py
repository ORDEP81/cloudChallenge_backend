import boto3
import json
import os


# create the client outside of the handler
DEFAULT_REGION = "us-east-1"
region_name = os.environ.get("AWS_REGION", DEFAULT_REGION)

def lambda_handler(event, context):
    dynamo = boto3.client('dynamodb', region_name='us-east-1')
    table_name = os.environ['TABLE_NAME']
    
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
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS" 
        },
    }
    return corsresponse    
    