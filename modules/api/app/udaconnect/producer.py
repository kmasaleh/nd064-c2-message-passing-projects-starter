import logging
from datetime import datetime
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer,KafkaConsumer
import json 

from modules.shared.kafka import TOPIC_NAME
from modules.shared.config import KAFKA_SERVER_ADDRESS
def create_topic(topic):
    try:
        consumer = KafkaConsumer(bootstrap_servers = KAFKA_SERVER_ADDRESS,security_protocol="PLAINTEXT")
        existing_topic_list = consumer.topics()
        if topic not in existing_topic_list:
            logging.warning ("udacconnect api server, create new topic ............")
            admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER_ADDRESS)
            topic_list = []
            topic_list.append(NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            logging.warning ("udacconnect api server, topic created ............")
        logging.warning ("udacconnect api server, topic already exist............")        
    except:
        logging.warning ("udacconnect api server, create topic exception......")        


def postPerson(payload):
    logging.warning ("udacconnect api server, produce new message ............")
    try:
        create_topic(TOPIC_NAME)
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER_ADDRESS,security_protocol="PLAINTEXT")
        producer.send(TOPIC_NAME,  json.dumps(payload).encode('utf-8'))
        producer.flush()
        logging.warning ("udacconnect api server, new message sent............")
    except:
        logging.warning ("udacconnect api server, post person exception........")