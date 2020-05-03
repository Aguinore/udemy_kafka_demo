from yaml_config_parser import ConfigParser


class Configs:
    def __init__(self):
        self.config = 'resources/config.yaml'
        yaml = ConfigParser(self.config)
        self.kafka_topic = yaml.get_config('kafka_topic')
        self.twitter_topics = yaml.get_config('twitter_topics')