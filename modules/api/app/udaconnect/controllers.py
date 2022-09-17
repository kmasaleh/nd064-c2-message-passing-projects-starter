import logging
from modules.shared.config import CONNECTIONS_SERVER_ADDRESS
import requests
import json

from sys import modules
from unicodedata import name
from unittest import result
from modules.shared.gRpcPersonsReader import gRpcReadPersons,gRpcReadPerson
from datetime import datetime

from modules.api.app.udaconnect.models import Connection, Location, Person
from modules.api.app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from modules.api.app.udaconnect.services import ConnectionService, LocationService, PersonService



from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
from modules.api.app.udaconnect.producer import postPerson

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        postPerson(payload)
        #new_person: Person = PersonService.create(payload)
        #return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] =[]
        personsList= gRpcReadPersons()
        for p in personsList.persons:
            person = Person()
            person.company_name = p.company_name
            person.first_name = p.first_name
            person.id = p.id
            person.last_name = p.last_name
            persons.append(person)
        return persons
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        p = gRpcReadPerson(person_id)
        person = Person()
        person.company_name = p.company_name
        person.first_name = p.first_name
        person.id = p.id
        person.last_name = p.last_name
        #person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    #@responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(request.args["start_date"], DATE_FORMAT)
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)
        url = f"http://{CONNECTIONS_SERVER_ADDRESS}/api/persons/{person_id}/connection?start_date={start_date.date()}&end_date={end_date.date()}&distance={distance}"
        r = requests.get(url,headers={'Connection':'close'})
        string = r.content.decode('utf-8')
        results = json.loads(string)

        #results= json.load(r);
        logger.info(results);
        print(results)
        return results

        """
        start_date: datetime = datetime.strptime(request.args["start_date"], DATE_FORMAT)
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        #we can make a connection microservice to retrieve person's connection based on id/sDate/eDate/diastance
        #we may impelment it by using gRpc
        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
        """
        
        
