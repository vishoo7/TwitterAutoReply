import sys
from time import ctime
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from credentials import *
from tweepy.utils import import_simplejson
import markovify
import random

json = import_simplejson()


class Listener(StreamListener):
    def __init__(self, api, followed_user_id, followed_user_handle, mock_mode):
        super().__init__(api)
        self.tweet_data = []
        self.followed_user_id = followed_user_id
        self.followed_user_handle = followed_user_handle

        self.mock_mode = mock_mode
        self.reply_list = []
        self.next_reply = ""
        self.load_next_reply(mock_mode)

    def on_error(self, error):
        print("Returned error code %s" % error)
        return False

    def on_status(self, status):
        if status.user.id == self.followed_user_id:
            tweet_text = '@%s %s' % (self.followed_user_handle, self.next_reply)
            self.api.update_status(tweet_text)

            print("%s: Tweeted:" % (ctime(), tweet_text))

            if self.mock_mode:
                self.update_mock_text(status.text)

            self.load_next_reply(self.mock_mode)

    def load_next_reply(self, mock=False):
        if not mock:
            with open('reply_list.txt', 'r') as reply_list_file:
                self.reply_list = reply_list_file.readlines()

            self.next_reply = random.choice(self.reply_list)

        else:
            with open("user_tweet_history.txt") as user_tweet_history_file:
                text = user_tweet_history_file.read()

            text_model = markovify.Text(text)
            self.next_reply = text_model.make_short_sentence(140)

    @staticmethod
    def update_mock_text(text):
        with open('user_tweet_history.txt', 'wa') as user_tweet_history_file:
            user_tweet_history_file.write(text)


if __name__ == "__main__":
    args = len(sys.argv)
    if args < 2:
        print('Need twitter handle (without @).')
        sys.exit()

    mock_mode = False
    if args == 3:
        mock_mode = sys.argv[2] == "1" or sys.argv[2].lower() == "true"

    followed_user_handle = sys.argv[1]

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    found_users = api.lookup_users(screen_names=[str(followed_user_handle)])

    if len(found_users) != 1:
        print('Lookup for twitter handle %s failed' % (followed_user_handle))
        sys.exit()

    followed_user_id = found_users[0].id

    twitterStream = Stream(auth, Listener(api, followed_user_id, followed_user_handle, mock_mode))
    twitterStream.filter(follow=[str(followed_user_id)], async=True)
