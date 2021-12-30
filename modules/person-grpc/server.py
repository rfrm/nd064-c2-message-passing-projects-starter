from concurrent import futures

import os
import time
import grpc
import logging
import person_service_pb2
import person_service_pb2_grpc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Person

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-person-grcp")

class PersonServicer(person_service_pb2_grpc.PersonServiceServicer):
    def create(self, request, context):
        logger.info('Got PersonCreation RPC message {}'.format(request))

        person = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }

        session = Session()
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        session.add(new_person)
        session.commit()

        logger.info('Saved new person')

        return person_service_pb2.PersonCreated(
            id=new_person.id,
            first_name=new_person.first_name,
            last_name=new_person.last_name,
            company_name=new_person.company_name
        )

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_service_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

logger.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
