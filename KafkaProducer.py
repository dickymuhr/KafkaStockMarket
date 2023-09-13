import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json

producer = KafkaProducer(bootstrap_servers=['16.171.153.102:9092'],
                         value_serializer = lambda x: dumps(x).encode('utf-8'))