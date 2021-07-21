import boto3
import pytest
from moto import mock_s3, mock_sqs

AWS_REGION = 'eu-central-1'
ITEM_TABLE = 'items'

STOCK_BUCKET = 'stocks'
STOCK_FILE = 'dummy-stocks.csv'

STOCK_QUEUE = 'stocks-queue'


@pytest.fixture(autouse=True)
def aws_config(monkeypatch):
    monkeypatch.setenv('AWS_DEFAULT_REGION', AWS_REGION)


@pytest.fixture
def s3_client():
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=STOCK_BUCKET, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})

        stocks = '''itemId;stock
1;1
2;1
3;2'''

        s3.put_object(Bucket=STOCK_BUCKET, Key=STOCK_FILE, Body=stocks.encode(encoding='utf-8'))

        yield s3


@pytest.fixture
def sqs_client():
    with mock_sqs():
        yield boto3.client('sqs')
