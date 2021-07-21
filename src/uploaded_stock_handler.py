import logging
from os import environ

import boto3

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def on_s3_event(event, context):
    s3 = boto3.client('s3')
    obj = s3.get_object(
        Bucket=event['Records'][0]['s3']['bucket']['name'],
        Key=event['Records'][0]['s3']['object']['key']
    )

    sqs = boto3.client('sqs')
    i = 0
    for line in obj['Body'].iter_lines():
        if i:
            sqs.send_message(QueueUrl=environ.get('STOCK_QUEUE_URL'),
                             MessageBody=line.decode('utf-8'))
        i += 1

    return {
        'processedLines': i - 1
    }
