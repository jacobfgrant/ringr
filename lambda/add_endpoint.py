"""Ringr Lambda Function – Add Endpoint

AWS Lambda function for adding an endpoint to Ringr. Adds endpoint to
SNS topic and includes endpoint info and ARN to DynamoDB database.

Author:  Jacob F. Grant
Created: 08/30/18
Updated: 09/09/18
"""


import os
from time import time
import boto3
from botocore.exceptions import ClientError

from utils import *


# Environmental Variables

try:
    DYNAMODB_TABLE = os.environ['dynamodb_table']
    TOPIC_ARN = os.environ['topic_arn']
    TTL = os.environ['ttl']
except KeyError as e:
    env_var_error = generate_api_response(
        500,
        "ERROR: Environmental variable " + str(e) + " not defined"
    )
else:
    env_var_error = None


# Client Objects

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns', region_name='us-east-1')


## HANDLER FUNCTION ##

def lambda_handler(event, context):
    """Handler function for AWS Lambda."""
    if(env_var_error):
        return env_var_error
        
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
