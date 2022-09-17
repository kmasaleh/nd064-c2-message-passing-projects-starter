
from datetime import datetime
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer,KafkaConsumer
import json 

TOPIC_NAME = 'test_kafka_topic'
KAFKA_SERVER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


def create_topic(topic):
    consumer = KafkaConsumer(bootstrap_servers = KAFKA_SERVER)
    existing_topic_list = consumer.topics()
    if topic not in existing_topic_list:
        print ("kafka persons api server, create new topic ............")
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)
        topic_list = []
        topic_list.append(NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print ("kafka persons api server, topic created ............")
    
    print ("kafka persons api server, topic already exist............")    

if __name__ == "__main__" :
    create_topic(TOPIC_NAME)
    print ("kafka persons api server, produce new message ............")
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    message = "date and time:" +date_time 
    producer.send(TOPIC_NAME,  json.dumps(message).encode('utf-8'))
    producer.flush()
    print ("kafka persons api server, new message sent............")


