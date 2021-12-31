import argparse
import grpc
import location_service_pb2
import location_service_pb2_grpc
import logging
import msgpack
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

parser = argparse.ArgumentParser(prog='send_location.py')
parser.add_argument('--person_id', nargs='?', required=True)
parser.add_argument('--latitude', nargs='?', required=True)
parser.add_argument('--longitude', nargs='?', required=True)
parser.add_argument('--creation_time', nargs='?', required=True)

args = parser.parse_args()

payload = {
    'person_id': int(args.person_id),
    'latitude': args.latitude,
    'longitude': args.longitude,
    'creation_time': args.creation_time
}

logger.info('Sending {}'.format(payload))

with grpc.insecure_channel(os.environ['LOCATION_GRPC']) as channel:
    stub = location_service_pb2_grpc.LocationServiceStub(channel)
    logging.info('Sending Location message')
    new_location = stub.RecordPersonLocation(location_service_pb2.Location(**payload))
