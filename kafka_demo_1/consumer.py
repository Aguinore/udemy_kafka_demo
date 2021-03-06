import sys
import json

from confluent_kafka.cimpl import KafkaError
from elasticsearch import Elasticsearch

from configs import Configs


def exit_gracefully(kafka_consumer):
    if kafka_consumer is not None:
        kafka_consumer.close()
        print('Consumer closed')
    sys.exit(0)


def create_kafka_consumer(topic):
    from confluent_kafka import Consumer

    settings = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'client.id': 'client-1',
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'}
    }

    c = Consumer(settings)

    c.subscribe([topic])

    return c


configs = Configs()
consumer = None

es = Elasticsearch(hosts=configs.elastic)

try:
    consumer = create_kafka_consumer(configs.kafka_topic)
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        elif not msg.error():
            tweet = msg.value()
            id = json.loads(tweet).get('id')
            es.index(index='twitter', doc_type='tweet', id=id, body=tweet)
            print('Received message: {0}'.format(tweet))
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))
finally:
    exit_gracefully(consumer)