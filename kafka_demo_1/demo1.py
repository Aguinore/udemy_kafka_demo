import twitter
from yaml_config_parser import ConfigParser


class Secrets:
    def __init__(self):
        self.config = 'resources/secret.yaml'
        yaml = ConfigParser(self.config)
        self.consumer_key = yaml.get_config('consumer_key')
        self.consumer_secret = yaml.get_config('consumer_secret')
        self.access_token_key = yaml.get_config('access_token_key')
        self.access_token_secret = yaml.get_config('access_token_secret')


secrets = Secrets()
api = twitter.Api(consumer_key=secrets.consumer_key,
                  consumer_secret=secrets.consumer_secret,
                  access_token_key=secrets.access_token_key,
                  access_token_secret=secrets.access_token_secret)