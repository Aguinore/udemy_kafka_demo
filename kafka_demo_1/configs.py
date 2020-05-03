from yaml_config_parser import ConfigParser


class Configs:
    def __init__(self):
        config = 'resources/config.yaml'
        yaml = ConfigParser(config)
        self.kafka_topic = yaml.get_config('kafka_topic')
        self.twitter_topics = yaml.get_config('twitter_topics')

        secret = 'resources/secret.yaml'
        yaml_secret = ConfigParser(secret)
        self.consumer_key = yaml_secret.get_config('consumer_key')
        self.consumer_secret = yaml_secret.get_config('consumer_secret')
        self.access_token_key = yaml_secret.get_config('access_token_key')
        self.access_token_secret = yaml_secret.get_config('access_token_secret')
        self.elastic = yaml_secret.get_config('elastic')