import json
from kafka import KafkaConsumer
TOPIC_NMAE = 'test_kafka_topic'
KAFKA_SERVER = 'localhost:9092'
consumer = KafkaConsumer(TOPIC_NMAE,bootstrap_servers=KAFKA_SERVER)

if __name__ == "__main__" :
    print ("Start listening:...................")
    for msg in consumer:
        #print (json.loads(msg.value))
        print (msg.value)