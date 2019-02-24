from kafka import KafkaProducer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import os
import logging
import logging.handlers
import json
from config import *


TWEETS_TOPIC = os.environ.get('TWEETS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda value: json.dumps(value).encode(),
)

class TweetStreamListener(StreamListener):

    def on_data(self, data):
        logger = logging.getLogger('twitter_stream')

        try:
            decoded = json.loads(data)
        except ValueError:
            logger.warn("Could not JSON decode Twitter response")
            return False

        tweet = ''
        try:
            tweet = decoded['text']
        except KeyError:
            logger.warn('No key text in Twitter response')
            return False

        print('twitter listener received:', tweet.encode('utf-8'))
        producer.send(TWEETS_TOPIC, value=tweet)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    print('generator started')

    listener = TweetStreamListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)

    stream.filter(track=['dog'])