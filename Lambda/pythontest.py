import os
import boto3
import unittest
from moto import mock_dynamodb2
from app import lambda_handler

def testCreds():  
  DEFAULT_REGION = "us-east-1"  
  os.environ['AWS_ACCESS_KEY_ID'] = 'foobar'
  os.environ['AWS_SECRET_ACCESS_KEY'] = 'foobar'
  os.environ['AWS_SECURITY_TOKEN'] = 'foobar'
  os.environ['AWS_SESSION_TOKEN'] = 'foobar' 
  os.environ["AWS_REGION"] = DEFAULT_REGION
 
  os.environ['TABLE_NAME'] = 'table_name' 

class testDynamo(unittest.TestCase): 
  @mock_dynamodb2
  def test_handler(self):
    dynamo = boto3.client('dynamodb')
    table_name = os.environ['TABLE_NAME']
    dynamo.create_table(
      TableName = table_name,
      BillingMode='PAY_PER_REQUEST',
      AttributeDefinitions=[
          {   
              'AttributeName': 'id',
              'AttributeType': 'S' 
          },
      ],
      KeySchema=[
          {
              'AttributeName': 'id',
              'KeyType': 'HASH'
          },
      ]
    )

    response = lambda_handler(0, 0)
    print("Response: ", response)

    self.assertEqual(200, response['statusCode'])

if __name__ == '__main__':
  testCreds()
  unittest.main() 
