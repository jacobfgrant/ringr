"""Ringr Lambda Function – Publish Notification

AWS Lambda function for publishing a message to the Ringr SNS topic. If
no message is included in the invocation, a default message is sent.

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
    DEFAULT_MESSAGE = os.environ['default_message']
    TOPIC_ARN = os.environ['topic_arn']
except KeyError as e:
    print("Warning: Environmental variable '" + str(e) + "' not defined")


# Client Objects

sns = boto3.client('sns', region_name='us-east-1')


## HANDLER FUNCTION ##

def lambda_handler(event, context):
    """Handler function for AWS Lambda."""
    # Check for required fields in request
    try:
        auth_key = event['auth_key']
    except KeyError as e:
        return generate_api_response(400, e)

    # Use default message if no message given
    try:
        sns_message = event['message']
    except KeyError:
        sns_message = DEFAULT_MESSAGE

    # Validate auth_key
    if not auth_function(auth_key):
        return generate_api_response(403, 'Authorization failed')

    # Publish SNS message
    sns_response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=sns_message,
        Subject='Ringr'
    )

    if (sns_response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return generate_api_response(
            sns_response['ResponseMetadata']['HTTPStatusCode'],
            "Error creating subscription"
        )

    return generate_api_response(200, "Success")


if __name__ == "__main__":
    pass
