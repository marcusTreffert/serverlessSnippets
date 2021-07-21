import logging
from os import environ

import boto3

__logger = logging.getLogger()
__logger.setLevel(logging.INFO)

def on_get(event, context):
    itemId = event['pathParameters'].get('itemId')

    table = boto3.resource('dynamodb').Table(environ.get('ITEM_TABLE'))

    result = table.get_item(Key={'itemId': itemId, 'sortKey': 'STOCK'})

    if result.get('Item', {}):
        stock = {
            'itemId': result['Item']['itemId'],
            'stock': int(result['Item']['stock'])
        }
    else:
        stock = None

    return stock
