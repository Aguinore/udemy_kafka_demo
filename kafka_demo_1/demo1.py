from tweepy import StreamListener, OAuthHandler, Stream
from yaml_config_parser import ConfigParser
import signal
import sys


class Secrets:
    def __init__(self):
        self.config = 'resources/secret.yaml'
        yaml = ConfigParser(self.config)
        self.consumer_key = yaml.get_config('consumer_key')
        self.consumer_secret = yaml.get_config('consumer_secret')
        self.access_token_key = yaml.get_config('access_token_key')
        self.access_token_secret = yaml.get_config('access_token_secret')


class StdOutListener(StreamListener):

    def __init__(self, kafka_producer):
        super().__init__()
        self.kafka_producer = kafka_producer

    """ A listener handles tweets that are received from the stream.
    """
    def on_data(self, data):
        self.kafka_producer.produce(topic='twitter_kafka', value=data)
        print(data)
        return True

    def on_error(self, status):
        print(status)


def exit_gracefully(kafka_producer):
    if kafka_producer is not None:
        kafka_producer.flush(30)
        print('kafka producer flushed')
    sys.exit(0)


def create_twitter_client(kafka_producer):
    listener = StdOutListener(kafka_producer)
    secrets = Secrets()
    auth = OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token_key, secrets.access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['python', 'gvido'])

    def signal_handler():
        print('You pressed Ctrl+C!')
        exit_gracefully(kafka_producer)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGKILL, signal_handler)
    return stream


def create_kafka_producer():
    # https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/
    from confluent_kafka import Producer

    p = Producer({'bootstrap.servers': 'localhost:9092',
                  'acks': 'all',
                  'enable.idempotence': True})
    return p


producer = None
try:
    producer = create_kafka_producer()
    create_twitter_client(producer)
finally:
    exit_gracefully(producer)