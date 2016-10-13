
import sys
from time import ctime
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from credentials import *
from tweepy.utils import import_simplejson
import random
json = import_simplejson()


class listener(StreamListener):
    def __init__(self, api, followed_user_id, followed_user_handle):
        self.tweet_data = []
        self.api = api
        self.followed_user_id = followed_user_id
        self.followed_user_handle = followed_user_handle

        self.reply_list = []
        self.next_reply = ""
        self.load_replies()

    def load_replies(self):
        with open('reply_list.txt', 'r') as reply_list_file:
            self.reply_list = reply_list_file.readlines()

        self.next_reply = random.choice(self.reply_list)

    def on_error(self, error):
        print("Returned error code %s" % error)
        return False

    def on_status(self, status):
        if status.user.id == self.followed_user_id:
            tweet_text = '@%s %s' % (self.followed_user_handle, self.next_reply)
            self.api.update_status(tweet_text)

            self.load_replies()
            print("%s: Tweeted:" % (ctime(), tweet_text))



if __name__ == "__main__":
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    followed_user_id = sys.argv[1]
    followed_user_handle = sys.argv[2]

    twitterStream = Stream(auth, listener(api, followed_user_id, followed_user_handle))
    twitterStream.filter(follow=[str(followed_user_id)], async=True)

