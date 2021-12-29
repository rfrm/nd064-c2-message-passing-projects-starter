import logging
import msgpack
from kafka import KafkaConsumer

from app.models import Location
from app.services import LocationService

TOPIC_NAME = 'udaconnect-locations'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=os.environ['KAFKA_SERVER'], value_deserializer=msgpack.unpackb)

for message in consumer:
    logging.info('Got location {}'.format(message.value))
    location: Location = LocationService.create(message.value)
    logging.info('Inserted location {} to database'.format(location.id))
