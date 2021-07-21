import logging
from os import environ

import boto3

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)


def on_sqs_event(event, context):

    lines = [msg['body'] for msg in event['Records']]

    table = boto3.resource('dynamodb').Table(environ.get('ITEM_TABLE'))

    i = 0
    for line in lines:
        fields = line.split(';')

        table.put_item(Item={
            'itemId': fields[0],
            'sortKey': 'STOCK',
            'stock': int(fields[1])
        })
        i += 1

    return {
        'processedStocks': i
    }
