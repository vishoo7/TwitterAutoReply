
from time import ctime
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from credentials import *
from tweepy.utils import import_simplejson
json = import_simplejson()


class listener(StreamListener):
    def __init__(self, api, followed_user):
        self.tweet_data = []
        self.api = api
        self.followed_user = followed_user

    def on_error(self, error):
        print("Returned error code %s" % error)
        return False

    def on_status(self, status):
        if status.user.id == self.followed_user:
            print("Tweeting at %s" % ctime())




if __name__ == "__main__":
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    followed_user = 25073877
    twitterStream = Stream(auth, listener(api, followed_user))
    twitterStream.filter(follow=[str(followed_user)], async=True)

