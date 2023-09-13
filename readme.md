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
**5. Change Advertised Listener Config**
```
    cd kafka_2.13-3.5.1
    sudo nano config/server.properties
```
- Change hostname to be Public IPv4 address of the AWS EC2 instance so that Kafka will expose itself through advertise.listener host and then other outside broker can communicate with it
```
    advertised.listeners=PLAINTEXT://your.host.name:9092
```
- This advertised.listener used by other broker (ex: local PC) to be address which is used to communicate with Kafka

**6. Start Zookeeper**
```
    bin/zookeeper-server-start.sh config/zookeeper.properties &
```
**7. Start Kafka**
```
    export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
```
```
    bin/kafka-server-start.sh config/server.properties &
```

- In case you wanna stop the server, use this command
```
    bin/kafka-server-stop.sh
    bin/zookeeper-server-stop.sh
```
**8. Edit Security Setting**
- This step allow request from local PC to AWS EC2 instance (not best practice for security)
- On your AWS EC2 instance go to Security -> Click on Security Group -> Edit inbound rules -> Add rule
    - Type: All traffic
    - Source: My IP

# Create Producer & Consumer
On local PC, install Kafka Python library
```
    pip install kafka-python
```