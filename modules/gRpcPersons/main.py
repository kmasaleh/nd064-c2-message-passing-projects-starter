import time
from concurrent import futures
import grpc



import logging
from datetime import datetime, timedelta
from typing import Dict, List

import os
import sys
#sys.path.append("E:\\Projects\\Workshop\\WebDev\\FullStack\\Udacity\\Cloud Native\\nd064-c2-message-passing-projects-starter-master")
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../')
sys.path.append(filename)


from modules.shared.models import db
from modules.shared.models import Connection, Location, Person
from modules.shared.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from modules.shared.services import  PersonService
import modules.shared.persons_pb2 as persons_pb2
import modules.shared.persons_pb2_grpc as persons_pb2_grpc

from modules.shared.config import config_by_name
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config_by_name[None or "test"])
db.init_app(app)
CORS(app)  # Set CORS for development

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("gRpcPersons-api")



class PersonsServicer(persons_pb2_grpc.PersonsServiceServicer):
    def GetAllPersons(self,request,context):
        logging.warning(f"getting persons from gRPC Persons Server...") 
        with app.app_context():
           persons: List[Person] = PersonService.retrieve_all()
           #persons: List[Person] =db.session.query(Person).all()
           result = persons_pb2.PersonsMessage();
           for  p in persons :
                person = persons_pb2.PersonMessage();
                person.id =  p.id
                person.first_name = p.first_name
                person.last_name  = p.last_name
                person.company_name = p.company_name
                result.persons.extend([person]) ;
        logging.warning("All persons returned from gRPC Persons Server...")
        return result

    def GetPerson(self,request,context):
        logging.warning(f"getting person from gRPC Persons Server...") 
        with app.app_context():
            p: Person = PersonService.retrieve(request.id)
            person = persons_pb2.PersonMessage();
            person.id =  p.id
            person.first_name = p.first_name
            person.last_name  = p.last_name
            person.company_name = p.company_name
            logging.warning(f"persons no {p.id} returned from gRPC Persons Server...")
            return person



def create_server(env=None):
    #initialize grpc server

    logging.warning (f"create  grpc persons api server  ..")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2));
    persons_pb2_grpc.add_PersonsServiceServicer_to_server(PersonsServicer(),server);
    logging.warning (f"grpc persons api server  adding port 5006..")
    server.add_insecure_port("[::]:5006")
    logging.warning (f"starting  grpc persons api server  ..")
    server.start()
    logging.warning("gRPC Persons Server Created @port 5006 SUCESSFULLY ....")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        logging.warning("gRPC Persons Server shut down ....")
        server.stop(0);

if __name__ == "__main__":
    create_server();