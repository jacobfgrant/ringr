"""Ringr Lambda Function – Remove Endpoint

AWS Lambda function for removing an endpoint from Ringr. Removes the
endpoint from the DynamoDB database; removing the endpoint from the SNS
topic is handled downstream by a separate function.

Author:  Jacob F. Grant
Created: 08/30/18
Updated: 09/09/18
"""


import os
import boto3
from botocore.exceptions import ClientError

from utils import *


# Environmental Variables

try:
    AUTH_KEY = os.environ['auth_key']
    DYNAMODB_TABLE = os.environ['dynamodb_table']
    TOPIC_ARN = os.environ['topic_arn']
except KeyError as e:
    print("Warning: Environmental variable '" + str(e) + "' not defined")


# Client Objects

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns', region_name='us-east-1')


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
