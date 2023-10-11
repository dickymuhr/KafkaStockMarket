from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json

consumer = KafkaConsumer(
    'stock',
    bootstrap_servers=['34.101.144.6:9093'],
    value_deserializer = lambda x: loads(x.decode('utf-8'))
)


for count, i in enumerate(consumer):
    json.dumps(i.value)
    print(f"Uploading {i.value}")