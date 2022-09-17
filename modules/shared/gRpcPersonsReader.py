import grpc
from modules.shared.config import GRPC_PERSONS_SERVER_ADDRESS
import modules.shared.persons_pb2 as pb
import modules.shared.persons_pb2_grpc as rpc
import logging


#channl =grpc.insecure_channel('host.docker.internal:30002');
def gRpcReadPersons():
    print(f"loading grpc channel {GRPC_PERSONS_SERVER_ADDRESS}")
    logging.warning(f"loading grpc channel {GRPC_PERSONS_SERVER_ADDRESS}")
    channl =grpc.insecure_channel(GRPC_PERSONS_SERVER_ADDRESS);
    stub = rpc.PersonsServiceStub(channel=channl);
    logging.warning(f"calling stub.GetAllPersons")
    response =  stub.GetAllPersons(pb .Empty());
    logging.warning(f"returning response from stub.GetAllPersons")
    return response


def gRpcReadPerson(id):
    print(f"loading grpc channel {GRPC_PERSONS_SERVER_ADDRESS}")
    logging.warning(f"loading grpc channel {GRPC_PERSONS_SERVER_ADDRESS}")
    channl =grpc.insecure_channel(GRPC_PERSONS_SERVER_ADDRESS);
    stub = rpc.PersonsServiceStub(channel=channl);
    personId = rpc.persons__pb2.PersonIdMessage()
    personId.id = int(id)
    logging.info(f"calling stub.GetPerson")
    response =  stub.GetPerson(personId);
    logging.warning(f"returning response from stub.GetPerson")
    return response
