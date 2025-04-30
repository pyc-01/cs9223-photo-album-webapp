import json
import os
import boto3
import requests
from datetime import datetime
from requests_aws4auth import AWS4Auth

def detect_labels(bucket, key):
    rek_cli = boto3.client('rekognition')
    response = rek_cli.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=10,
        MinConfidence=70
    )
    return response['Labels']

def get_metadata(bucket, key):
    s3_cli = boto3.client('s3')
    response = s3_cli.head_object(Bucket=bucket, Key=key)
    return response['Metadata']

def es_insert(json_obj):
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, 'us-east-1', 'es', session_token=credentials.token)
    
    url = host + 'photos/' + '_doc/' + json_obj['object_key']
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        url, auth=awsauth, headers=headers, json=json_obj)

    return response

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    labels = detect_labels(bucket, key)
    metadata = get_metadata(bucket, key)

    if metadata['customLabels'] == '':
        custom_labels = []
    else:
        custom_labels = metadata['customLabels'].split(',')

    labels_list = [l['Name'] for l in labels] + custom_labels

    json_obj = {
        "object_key": key,
        "bucket": bucket,
        "createdTimestamp": datetime.now().isoformat(),
        "labels": labels_list
    }

    res = es_insert(json_obj)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
