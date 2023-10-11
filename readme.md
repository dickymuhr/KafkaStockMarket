# Kafka Stock Market Project
Project based on Darshil Parmar Youtube Video [Stock Market Real-Time Data Analysis Using Kafka](https://www.youtube.com/watch?v=KerNf0NANMo).
Here we will create Kafka Streaming project that produce stock market data from an API, consume it to the Google Cloud Storage. Then query it in Google BigQuery.

What is Kafka? Learn here [Kafka Visualizaiton](https://softwaremill.com/kafka-visualisation/)
# Architechture

![Alt text](gcp-arch.png "Architechture")
# Steps
**1. [Installing Kafka on GCE](#installing-kafka-on-GCE)**

**2. [Create Producer](#create-producer)**

**3. [Create Consumer](#create-consumer)**

**4. [Running Producer and Consumer](#running-producer-and-consumer)**



# Installing Kafka on GCE
**1. Create Instance & Access Through SSH**
- Create Compute Engine VM on Google Cloud Platform
    - Operating System: Ubuntu
    - Access scopes: Allow full access to all Cloud APIs
    - Fireall: Allow HTTP traffic, Allow HTTPS traffic
- On local terminal, [create SSH Key](https://cloud.google.com/compute/docs/connect/create-ssh-keys)
```bash
ssh-keygen -t rsa -f ~/.ssh/FILENAME -C USERNAME -b 2048
```
- Add public key in `~/.ssh/FILENAME.pub` to `Compute Engine/Metadata/SSH KEYS/ADD SSH KEY`
- Login to VM via SSH from local terminal, specify the VM External IP Address
```bash
ssh -i ~/.ssh/FILENAME USERNAME@EXTERNAL_IP
```

- Some tips for keeping SSH session alive [here](https://unix.stackexchange.com/questions/200239/how-can-i-keep-my-ssh-sessions-from-freezing)

**2. Install Kafka**
- In VM, download latest kafka version [here](https://kafka.apache.org/downloads)
```bash
wget https://downloads.apache.org/kafka/3.5.1/kafka_2.13-3.5.1.tgz
tar -xvf kafka_2.13-3.5.1.tgz
```
- Install Java
```bash
sudo apt-get update
sudo apt-get install openjdk-8-jdk
java -version
```
- Change Listener Config
```bash
cd kafka_2.13-3.5.1
sudo nano config/server.properties
```
- Change this settings, it configure where the client should communicate (within or outside GCE), change the `EXTERNAL_IP`
```bash
listeners=INTERNAL://0.0.0.0:9092,EXTERNAL://0.0.0.0:9093
advertised.listeners=INTERNAL://localhost:9092,EXTERNAL://EXTERNAL_IP:9093
listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
inter.broker.listener.name=INTERNAL
```
**3. Create Custom Firewall Rule**
- Navigate to `VPC network/Firewall/CREATE FIREWALL RULE`
- Give your rule a name, and under "Targets", select "All instances in the network".
- Under "Source IP ranges", input `YOUR_IP_ADDRESS`/32 to allow traffic from your local terminal. Check your IP [here](http://whatismyip.akamai.com/) 
- Under "Protocols and ports", select "Specified protocols and ports", then mark TCP and input `9092,9093` to allow TCP traffic on ports 9092 and 9093
- Check if it is works
```bash
telnet EXTERNAL_IP 9093
```

# Create Producer
**1. Install Kafka Python Library**
- Install on local terminal
```bash
pip install kafka-python
```
**2. Create KafkaProducer.py as producer script**
- Don't forget to change the `EXTERNAL IP`
```python
from kafka import KafkaProducer
import os, json
from dotenv import load_dotenv
import time
import finnhub

# Define producer
producer = KafkaProducer(bootstrap_servers=['EXTERNAL_IP:9093'],
                         value_serializer = lambda x: json.dumps(x).encode('utf-8'))
                        # why do we need utf-8 encoding? because kafka need byte string, not regular string

# Define finnhub client
load_dotenv(dotenv_path='key/finnhub.env') # Load the .env file
api_key = os.getenv('FINNHUB_API_KEY') # Get the API key
finnhub_client = finnhub.Client(api_key=api_key)

# Define request function
def getStock(symbol):
    stock_quote = {}
    try:
        stock_quote = finnhub_client.quote(symbol)
        stock_quote["symbol"] = symbol
    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
    return stock_quote

stock_symbols = ['NVDA', 'AMZN', 'GOOGL', 'MSFT']
while True:
    for symbol in stock_symbols:
        try:
            stock_dict = getStock(symbol)
            producer.send("stock", value=stock_dict)
            print(f"Sending: {json.dumps(stock_dict, indent=2)}")
        except Exception as e:
            print(f"Producer error: {e}")
    time.sleep(60)

```

# Create Consumer

