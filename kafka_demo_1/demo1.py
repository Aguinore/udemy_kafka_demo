from tweepy import StreamListener, OAuthHandler, Stream
from yaml_config_parser import ConfigParser


class Secrets:
    def __init__(self):
        self.config = 'resources/secret.yaml'
        yaml = ConfigParser(self.config)
        self.consumer_key = yaml.get_config('consumer_key')
        self.consumer_secret = yaml.get_config('consumer_secret')
        self.access_token_key = yaml.get_config('access_token_key')
        self.access_token_secret = yaml.get_config('access_token_secret')


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


def create_twitter_client():
    l = StdOutListener()
    secrets = Secrets()
    auth = OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token_key, secrets.access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['python', 'gvido'])


client = create_twitter_client()
#create a kafka producer
#loop to send tweets to kafka