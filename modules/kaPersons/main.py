import logging
import json

import os
import sys
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../')
sys.path.append(filename)


from modules.shared.services import  PersonService
from modules.shared.models import db,Person
from modules.shared.config import config_by_name,KAFKA_SERVER_ADDRESS

from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from modules.shared.kafka import TOPIC_NAME

from flask import Flask
app = Flask(__name__)
app.config.from_object(config_by_name[None or "test"])
db.init_app(app)


def create_topic(topic):
    try:
        consumer = KafkaConsumer(bootstrap_servers = KAFKA_SERVER_ADDRESS,security_protocol="PLAINTEXT")
        #consumer = KafkaConsumer(bootstrap_servers = KAFKA_SERVER)
        existing_topic_list = consumer.topics()
        if topic not in existing_topic_list:
            print ("kafka persons api server, create new topic ............")
            admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER_ADDRESS)
            topic_list = []
            topic_list.append(NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print ("kafka persons api server, topic created ............")
        
        print ("kafka persons api server, topic already exist............")    
    except:
        print ("kafka persons api server, create topic exception......")        

def run_server():
    logging.warning (f"Start kafka persons api server  {KAFKA_SERVER_ADDRESS}.......")
    create_topic(TOPIC_NAME)    
    consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers = [KAFKA_SERVER_ADDRESS])
    logging.warning ("Start listening on persons_post_topic .............")
    for msg in consumer:
        logging.warning ("A message arrived on persons api server ............")
        try:
            payload = json.loads(msg.value)
            with app.app_context():
                new_person: Person = PersonService.create(payload)
                logging.warning (f"kafka persons api server, new person created  {new_person}....")
        except:
            logging.warning (f"kafka persons api server, create person exception")

if __name__ == "__main__" :
    run_server()            

