import boto3
import os
import unittest
from app import lambda_handler
from moto import mock_dynamodb2


def aws_setup():  
  #Mocked AWS Credentials for moto  
  os.environ['AWS_ACCESS_KEY_ID'] = 'foobar'
  os.environ['AWS_SECRET_ACCESS_KEY'] = 'foobar'
  os.environ['AWS_SECURITY_TOKEN'] = 'foobar'
  os.environ['AWS_SESSION_TOKEN'] = 'foobar' 
  os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
 
  # Database table name into env variable   
os.environ['TABLE_NAME'] = 'table_name' 

class TestLambdaDDB(unittest.TestCase): 
  @mock_dynamodb2
  def test_handler(self):
    # Create dynamodb boto3 object
    dynamo = boto3.client('dynamodb')
    # Get dynamodb table name from env
    table_name = os.environ['TABLE_NAME']
    
    # Create mock table
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

    # Print Lambda response
    LambdaResponse = lambda_handler(0, 0)
    print("Lambda response: ", LambdaResponse)

    # Run unit test against Lambda status code
    self.assertEqual(200, LambdaResponse['statusCode'])

if __name__ == '__main__':
  aws_setup()
  unittest.main() 