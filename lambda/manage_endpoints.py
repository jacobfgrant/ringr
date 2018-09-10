"""Ringr Lambda Function – Manage Endpoints

AWS Lambda function for managing endpoints based on events in the Ringr
DynamoDB table. Depending on the action recorded in the DynamoDB
database stream, this function will do one of several things:

- INSERT: If an endpoint has been added to the DynamoDB database, no
    action is taken.

- MODIFIY: If an endpoint has been modified in the DynamoDB database
    (and it's ARN has changed) the old endpoint ARN will be removed from
    the SNS topic.

- REMOVE: If an endpoint has been removed from the DynamoDB database, it
    is removed from the SNS topic.

Author:  Jacob F. Grant
Created: 08/30/18
Updated: 09/09/18
"""


import os

import boto3
from botocore.exceptions import ClientError


# Environmental Variables

try:
    TOPIC_ARN = os.environ['topic_arn']
except KeyError as e:
    env_var_error = generate_api_response(
        500,
        "ERROR: Environmental variable " + str(e) + " not defined"
    )
else:
    env_var_error = None


# Client Objects

sns = boto3.client('sns', region_name='us-east-1')


## HANDLER FUNCTION ##

def lambda_handler(event, context):
    """Handler function for AWS Lambda."""
    if(env_var_error):
        return env_var_error
        
    results = []
    dynamodb_stream_records = event['Records']

    # Loop through records from DynamoDB stream
    for record in dynamodb_stream_records:
        response = None

        # Ignore INSERT event
        if(record['eventName'] == 'INSERT'):
            continue

        # For MODIFY event, check if ARN is changed
        if(record['eventName'] == 'MODIFY'):
            try:
                new_arn = record['dynamodb']['NewImage']['arn']['S']
                old_arn = record['dynamodb']['OldImage']['arn']['S']
            except KeyError as e:
                results.append("ERROR: " + str(e) + " not found")
                continue

            if(new_arn != old_arn):
                response = sns.unsubscribe(
                    SubscriptionArn=old_arn
                )
     
        # For REMOVE event, unsubscribe from SNS
        if(record['eventName'] == 'REMOVE'):
            try:
                subscription_arn = record['dynamodb']['OldImage']['arn']['S']
            except KeyError as e:
                results.append("ERROR: " + str(e) + " not found")
                continue

            response = sns.unsubscribe(
                SubscriptionArn=subscription_arn
            )

        if(response):
            results.append(response)

    return results


if __name__ == "__main__":
    pass
