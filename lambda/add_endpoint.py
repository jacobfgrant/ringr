"""Ringr Lambda Function – Add Endpoint

AWS Lambda function for adding an endpoint to Ringr. Adds endpoint to
SNS topic and includes endpoint info and ARN to DynamoDB database.

Author:  Jacob F. Grant
Created: 08/30/18
Updated: 09/07/18
"""


import os
import re
from time import time

import boto3
from botocore.exceptions import ClientError


try:
    AUTH_KEY = os.environ['auth_key']
    DYNAMODB_TABLE = os.environ['dynamodb_table']
    TOPIC_ARN = os.environ['topic_arn']
    TTL = os.environ['ttl']
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

    # Add subscription to SNS topic
    sns_response = sns.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol=protocol,
        Endpoint=endpoint,
        ReturnSubscriptionArn=True
    )

    if (sns_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            sns_response['ResponseMetadata']['HTTPStatusCode'],
            "Error creating subscription"
        )

    # Add subscription info to DynamoDB table
    try:
        ttl = str(int(time()) + int(TTL))
    except ValueError:
        ttl = str(int(time()) + 3600)

    dynamodb_item = {
        "arn": {"S": sns_response['SubscriptionArn']},
        "endpoint": {"S": endpoint},
        "protocol": {"S": protocol},
        "ttl": {"N": ttl}
    }

    dynamodb_response = dynamodb.put_item(
        TableName=DYNAMODB_TABLE,
        Item=dynamodb_item
    )

    if (dynamodb_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            dynamodb_response['ResponseMetadata']['HTTPStatusCode'],
            "Error creating database record"
        )

    return generate_api_response(200, "Success")


if __name__ == "__main__":
    pass
