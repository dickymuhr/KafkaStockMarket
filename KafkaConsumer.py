from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json
from google.cloud import storage

# Initialize consumer
consumer = KafkaConsumer(
    'stock',
    bootstrap_servers=['34.101.144.6:9093'],
    value_deserializer = lambda x: loads(x.decode('utf-8'))
)

# Initialize a GCS client
bucket_name = 'kafka-stock-quote'
storage_client = storage.Client.from_service_account_json('key/kafka-streaming-401702-8a5417c45fd7.json')
bucket = storage_client.bucket(bucket_name)

for message in consumer:
    filename = message.value['t']
    symbol = message.value['symbol']

    blob_name = f'stock_market_{filename}_{symbol}.json'
    blob = bucket.blob(blob_name)

    # Convert message value to JSON string
    json_data = json.dumps(message.value)
    # Upload the data
    blob.upload_from_string(json_data)
    print(f"Uploading {message.value}")