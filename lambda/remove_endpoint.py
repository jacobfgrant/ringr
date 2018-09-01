"""Ringr Lambda Function – Remove Endpoint

AWS Lambda function for removing an endpoint from Ringr. Removes the
endpoint from the DynamoDB database; removing the endpoint from the SNS
topic is handled downstream by a separate function.

Author:  Jacob F. Grant
Created: 08/30/18
Updated: 09/07/18
"""


import os

import boto3
from botocore.exceptions import ClientError


try:
    AUTH_KEY = os.environ['auth_key']
    DYNAMODB_TABLE = os.environ['dynamodb_table']
    TOPIC_ARN = os.environ['topic_arn']
except KeyError as e:
    print("Warning: Environmental variable '" + str(e) + "' not defined")


dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns', region_name='us-east-1')


# General Functions

def auth_function(key):
    """Check if authorization key is valid."""
    if(key == AUTH_KEY):
        return True
    else:
        return False


def generate_api_response(response_code, body):
    """Return a properly formatted API response."""
    api_response = {
        "isBase64Encoded": False,
        "statusCode": response_code,
        "headers": { "Content-Type": "application/json"},
        "body": body
    }
    return api_response


def sanitize_endpoint_input(endpoint):
    """Sanitize endpoint and return SNS protocol."""
    endpoint = ('').join(re.split(r'\-|\(|\)|\s', endpoint))
    try:
        endpoint = str(int(endpoint))
    except ValueError:
        return None, None

    if(len(endpoint) == 10):
        endpoint = '1' + endpoint

    if(len(endpoint) == 11 and endpoint[0] == '1'):
        return endpoint, 'sms'
    
    return None, None


## HANDLER FUNCTION ##

def lambda_handler(event, context):
    """Handler function for AWS Lambda."""
    # Check for required fields in request
    try:
        auth_key = event['auth_key']
        endpoint = event['endpoint']
    except KeyError as e:
        return generate_api_response(400, e)

    # Validate auth_key
    if not auth_function(auth_key):
        return generate_api_response(403, 'Authorization failed')

    # Parse endpoint and protocol
    endpoint, protocol = sanitize_endpoint_input(endpoint)
    if(not endpoint or not protocol):
        return generate_api_response(400, 'Endpoint not valid phone number')


    # Get endpoint info from DynamoDB
    dynamodb_get_response = dynamodb.get_item(
        TableName=DYNAMODB_TABLE,
        Key={"endpoint": {"S": endpoint}}
    )

    if (dynamodb_get_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            dynamodb_get_response['ResponseMetadata']['HTTPStatusCode'],
            "Error fetching database record"
        )

    subscription_arn = dynamodb_get_response['Item']['arn']['S']

    # Delete SNS subscription
    sns_response = sns.unsubscribe(
        SubscriptionArn=subscription_arn
    )

    if (sns_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            sns_response['ResponseMetadata']['HTTPStatusCode'],
            "Error creating subscription"
        )

    # Delete DynamoDB record
    dynamodb_delete_response = dynamodb.delete_item(
        TableName=DYNAMODB_TABLE,
        Key={"endpoint": {"S": endpoint}}
    )

    if (dynamodb_delete_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            dynamodb_delete_response['ResponseMetadata']['HTTPStatusCode'],
            "Error deleting database record"
        )

    return generate_api_response(200, "Success")


if __name__ == "__main__":
    pass
