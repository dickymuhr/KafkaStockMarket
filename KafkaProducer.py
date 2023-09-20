import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json

producer = KafkaProducer(bootstrap_servers=['13.51.196.19:9093'],
                         value_serializer = lambda x: dumps(x).encode('utf-8'))
                        # why do we need utf-8 encoding? because kafka need byte string, not regular string

df = pd.read_csv('indexProcessed.csv')

while True:
    stock_dict = df.sample(1).to_dict(orient="records")[0]
    producer.send("stock", value=stock_dict)
    print(f"sending {stock_dict}")
    sleep(5)
