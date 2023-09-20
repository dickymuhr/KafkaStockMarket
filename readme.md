# Kafka Stock Market Project
Project based on Darshil Parmar Youtube Video [Stock Market Real-Time Data Analysis Using Kafka](https://www.youtube.com/watch?v=KerNf0NANMo)

What is Kafka? Learn here [Kafka Visualizaiton](https://softwaremill.com/kafka-visualisation/)
# Architechture

![Alt text](architechture.jpg "Architechture")
Image from [here](https://github.com/darshilparmar/stock-market-kafka-data-engineering-project)
# Steps
**1. [Installing Kafka on AWS EC2](#installing-kafka-on-aws-ec2)**

**2. [Create Producer & Consumer](#make-producer--consumer)**


# Installing Kafka on AWS EC2
**1. Launch new AWS EC2 instance**
- Named it "kafka-stock-market-project". Choose Ubuntu AMI. Don't forget to create key pair and save it 
**2. Login with SSH client**
- Go to folder where you save .pem file. Then change the permision to read-only
```
    chmod 400 kafka-stock-market-project.pem
```

- Then login with SSH, change ec2-instance with your own instance

```
    ssh -i "kafka-stock-market-project.pem" ec2-instance
```
**3. Download Apache Kafka**
- Check latest kafka version [here](https://kafka.apache.org/downloads)
```
    wget https://downloads.apache.org/kafka/3.5.1/kafka_2.13-3.5.1.tgz
    tar -xvf kafka_2.13-3.5.1.tgz
```
**4. Install Java**
```
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk
    java -version
```
**5. Change Listener Config**
```
    cd kafka_2.13-3.5.1
    sudo nano config/server.properties
```
- Change this settings, it configure where the client should communicate (within or outside EC2)
```
    listeners=INTERNAL://0.0.0.0:9092,EXTERNAL://0.0.0.0:9093
    advertised.listeners=INTERNAL://172.31.47.74:9092,EXTERNAL://13.51.196.19:9093
    listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
    inter.broker.listener.name=INTERNAL
```
- This advertised.listener used by other broker (ex: local PC) to be address which is used to communicate with Kafka

**Side Note**
- In general, the address in the **advertised.listeners** configuration is the one Kafka uses for all outbound communications and the one it tells clients and other brokers to use for inbound communications.
- This **listener** configuration determines on which network interfaces and ports the Kafka broker will accept incoming connections.

**6. Start Zookeeper**
```
    bin/zookeeper-server-start.sh config/zookeeper.properties 
```
**7. Start Kafka**
```
    export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
```
```
    bin/kafka-server-start.sh config/server.properties 
```

- In case you wanna stop the server, use this command
```
    bin/kafka-server-stop.sh
    bin/zookeeper-server-stop.sh
```
**8. Edit Security Setting**
- This step allow all request from local PC to AWS EC2 instance (not best practice for security)
- On your AWS EC2 instance go to Security -> Click on Security Group -> Edit inbound rules -> Add rule
    - Type: All traffic
    - Source: My IP

**8. Create Topic**
```
    bin/kafka-topics.sh --create --topic demo_testing --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```
- Or it will automatically created when Kafka Producer send message to the Kafka broker

- To List topics
```
    bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

# Create Producer & Consumer
**1. On local PC, install Kafka Python library**
```
    pip install kafka-python
```

**2. Create KafkaProducer.py to make dummy producer using csv stock market data**
```
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
        sleep(1)
```