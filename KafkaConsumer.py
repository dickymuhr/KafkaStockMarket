import pandas as pd
from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json

consumer = KafkaConsumer(
    bootstrap_servers=['16.171.153.102:9092'],
    value_deserializer = lambda x: loads(x.decode('utf-8'))
    # why do we need utf-8?
)