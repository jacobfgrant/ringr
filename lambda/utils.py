"""General Utilities and Functions for Ringr

A collection of shared utilities and functions for Ringr.

Author:  Jacob F. Grant
Created: 09/09/18
Updated: 09/09/18
"""


import os
import re


## General Functions

def auth_function(key):
    """Check if authorization key is valid."""
    try:
        if(key == os.environ['auth_key']):
            return True
    except:
        pass
    else:
        return False


def generate_api_response(response_code, body):
    """Return a properly formatted API response."""
    api_response = {
        "isBase64Encoded": False,
        "statusCode": response_code,
        "headers": {"Content-Type": "application/json"},
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


if __name__ == "__main__":
    pass
