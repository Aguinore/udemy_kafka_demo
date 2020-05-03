from tweepy import StreamListener, OAuthHandler, Stream
from configs import Configs
import sys


class StdOutListener(StreamListener):

    def __init__(self, kafka_producer, topic):
        super().__init__()
        self.kafka_producer = kafka_producer
        self.topic = topic

    """ A listener handles tweets that are received from the stream.
    """
    def on_data(self, data):
        self.kafka_producer.produce(topic=self.topic, value=data)
        print(data)
        return True

    def on_error(self, status):
        print(status)


def exit_gracefully(kafka_producer):
    if kafka_producer is not None:
        kafka_producer.flush(30)
        print('kafka producer flushed')
    sys.exit(0)


def create_twitter_client(kafka_producer, configs):
    listener = StdOutListener(kafka_producer, configs.kafka_topic)
    auth = OAuthHandler(configs.consumer_key, configs.consumer_secret)
    auth.set_access_token(configs.access_token_key, configs.access_token_secret)

    return Stream(auth, listener)


def create_kafka_producer():
    # https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/
    from confluent_kafka import Producer

    p = Producer({'bootstrap.servers': 'localhost:9092',
                  'acks': 'all',
                  'enable.idempotence': 'true',
                  'compression.type': 'snappy'})
    return p


configs = Configs()
producer = None
try:
    producer = create_kafka_producer()
    client = create_twitter_client(producer, configs)

    client.filter(track=configs.twitter_topics)

finally:
    exit_gracefully(producer)
