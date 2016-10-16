#!/usr/bin/env python3.5

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
import argparse

json = import_simplejson()


class Listener(StreamListener):
    def __init__(self, api, followed_user_id, followed_user_handle, mock_mode):
        super().__init__(api)
        self.tweet_data = []
        self.followed_user_id = followed_user_id
        self.followed_user_handle = followed_user_handle

        self.mock_mode = mock_mode
        self.reply_list = []
        self.next_reply = ''
        self.load_next_reply(mock_mode)

    def on_error(self, error):
        print("Returned error code %s" % error)
        return False

    def on_status(self, status):
        if status.user.id == self.followed_user_id:
            tweet_text = '@%s %s' % (self.followed_user_handle, self.next_reply)
            self.api.update_status(tweet_text, in_reply_to_status_id=status.id)

            print('%s: Tweeted: %s' % (ctime(), tweet_text))

            if self.mock_mode:
                self.update_mock_text(status.text)

            self.load_next_reply(self.mock_mode)

    def load_next_reply(self, mock=False):
        if not mock:
            with open('reply_list.txt', 'r') as reply_list_file:
                self.reply_list = reply_list_file.readlines()

            self.next_reply = random.choice(self.reply_list)

        else:
            with open('user_tweet_history.txt') as user_tweet_history_file:
                text = user_tweet_history_file.read()

            text_model = markovify.Text(text)
            self.next_reply = text_model.make_short_sentence(140)

    @staticmethod
    def update_mock_text(text):
        with open('user_tweet_history.txt', 'wa') as user_tweet_history_fd:
            user_tweet_history_fd.write(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--handle',
                        required=True,
                        type=str,
                        dest='followed_handle',
                        action='store',
                        help='Twitter handle (without @)')
    parser.add_argument('--mock',
                        dest='mock_mode',
                        default=False,
                        action='store_true',
                        help='enable mock mode')
    args = parser.parse_args()

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    found_users = api.lookup_users(screen_names=[str(args.followed_handle)])

    if len(found_users) != 1:
        print('Lookup for twitter handle %s failed' % args.followed_handle)
        sys.exit()

    followed_user_id = found_users[0].id

    twitterStream = Stream(auth, Listener(api, followed_user_id, args.followed_handle, args.mock_mode))
    twitterStream.filter(follow=[str(followed_user_id)], async=True)
