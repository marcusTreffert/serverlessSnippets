import pytest

from src.tests.conftest import STOCK_BUCKET, STOCK_FILE, STOCK_QUEUE
from src.uploaded_stock_handler import on_s3_event


@pytest.fixture(autouse=True)
def before(monkeypatch, s3_client, sqs_client):
    finished_orders_queue = sqs_client.create_queue(QueueName=STOCK_QUEUE)
    monkeypatch.setenv('STOCK_QUEUE_URL', finished_orders_queue.get('QueueUrl'))


def test_on_s3_event_ok():
    event = {
        'Records': [{'s3': {'bucket': {'name': STOCK_BUCKET}, 'object': {'key': STOCK_FILE}}}]
    }

    response = on_s3_event(event, None)

    assert response
    assert response.get('processedLines') == 3
