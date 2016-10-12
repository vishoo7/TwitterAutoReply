
import time
import os
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from credentials import *


class listener(StreamListener):
    def __init__(self, api, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        self.api = api

    def on_status(self, status):
        print(status.text)



if __name__ == "__main__":
    start_time = time.time()  # grabs the system time
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    twitterStream = Stream(auth, listener(api, start_time, time_limit=20))  # initialize Stream object with a time out limit
    twitterStream.filter(follow=['25073877'],async=True)

