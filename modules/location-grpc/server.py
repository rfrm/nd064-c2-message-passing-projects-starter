from concurrent import futures

import os
import time
import grpc
import msgpack
import logging
import location_service_pb2
import location_service_pb2_grpc

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-grcp")
location_producer = KafkaProducer(bootstrap_servers=os.environ['KAFKA_SERVER'], value_serializer=msgpack.dumps)

class LocationServicer(location_service_pb2_grpc.LocationServiceServicer):
    def RecordPersonLocation(self, request, context):
        logger.info('Got Location RPC message {}'.format(request))

        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "creation_time": request.creation_time,
        }

        location_producer.send('udaconnect-locations', location)
        location_producer.flush()
        logger.info("Published location to Kakfa")

        return location_service_pb2.SavedLocationStatus(status="published")

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_service_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

logger.info("Server starting on port 5006...")
server.add_insecure_port("[::]:5006")
server.start()
server.wait_for_termination()
