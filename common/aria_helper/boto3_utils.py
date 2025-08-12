# This module contains utility functions for interacting with AWS services using the Boto3 library.

import json
import boto3
from bson import ObjectId
from datetime import datetime
from botocore.exceptions import ClientError
import os

region_name = os.environ['REGION']
if not region_name:
    raise ValueError("Env value 'region_name' not found.")


def get_secret(secret_name, return_json=True):
    """
    This function retrieves the secret value from AWS Secrets Manager.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"An error occurred while retrieving the secret value for {secret_name}: {e}")
        raise e

    secret = get_secret_value_response['SecretString']
    if return_json:
        return json.loads(secret)

    return secret


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S')

    return o


def trigger_lambda(function_name, payload):
    # Create an AWS Lambda client
    client = boto3.client('lambda', region_name=region_name)

    # Define the parameters for the async invocation
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=(
            json.dumps(payload, default=json_encoder)
        ).encode('utf-8')
    )

    return response


def trigger_lambda_response(function_name, payload):
    # Create an AWS Lambda client
    client = boto3.client('lambda', region_name=region_name)

    # Define the parameters for the async invocation
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=(
            json.dumps(payload, default=json_encoder)
        ).encode('utf-8')
    )

    return response


def post_to_s3(body, bucket, key, filename):
    # Upload the log message to S3
    s3 = boto3.client('s3', region_name=region_name)

    # Upload the log file to S3
    s3.put_object(Body=body, Bucket=bucket, Key=f"{key}/{filename}")


def get_from_s3(bucket, key):
    s3 = boto3.client('s3', region_name=region_name)
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()
