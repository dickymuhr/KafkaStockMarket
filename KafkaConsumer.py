from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json
from s3fs import S3FileSystem

consumer = KafkaConsumer(
    'stock',
    bootstrap_servers=['13.51.196.19:9093'],
    value_deserializer = lambda x: loads(x.decode('utf-8'))
)

s3 = S3FileSystem()

for count, i in enumerate(consumer):
    with s3.open("s3://kafka-stock-market-diccode/stock_market_{}.json".format(count), 'w') as file:
        json.dump(i.value,file)