#!/usr/bin/env python3.5

import sys
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from credentials import *
from utils import gen_hashtags
import markovify
import random
import argparse
import logging

log = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s'))
stdout_handler.setLevel(logging.INFO)
log.addHandler(stdout_handler)
log.setLevel(logging.INFO)

class Listener(StreamListener):
    def __init__(self, api, followed_user_id, followed_user_handle, mock_mode, hashtags):
        super().__init__(api)
        self.tweet_data = []
        self.followed_user_id = followed_user_id
        self.followed_user_handle = followed_user_handle

        self.mock_mode = mock_mode
        self.reply_list = []
        self.next_reply = ''
        self.load_next_reply(mock_mode, hashtags)

    def on_error(self, error):
        log.error("Returned error code %s" % error)
        return False

    def on_status(self, status):
        if status.user.id == self.followed_user_id:
            tweet_text = '@%s %s' % (self.followed_user_handle, self.next_reply)
            self.api.update_status(tweet_text, in_reply_to_status_id=status.id)

            log.info('%s tweeted: %s' % (self.followed_user_handle, status.text))
            log.info('Tweeted: %s' % tweet_text)

            if self.mock_mode:
                self.update_mock_text(status.text)

            self.load_next_reply(self.mock_mode, hashtags)

    def load_next_reply(self, mock=False, hashtags=None):
        hashtag_string = gen_hashtags(hashtags)

        if not mock:
            with open('reply_list.txt', 'r') as reply_list_file:
                self.reply_list = reply_list_file.readlines()

            reply = random.choice(self.reply_list)
            if hashtags:
                reply += ' ' + hashtag_string
            self.next_reply = reply

        else:
            with open('user_tweet_history.txt') as user_tweet_history_file:
                text = user_tweet_history_file.read()

            text_model = markovify.NewlineText(text)
            if hashtags:
                reply = text_model.make_short_sentence(140 - (len(hashtag_string) + 1), tries=30).upper()
                reply += ' ' + hashtag_string
            else:
                reply = text_model.make_short_sentence(140, tries=30).upper()
            self.next_reply = reply

        log.info('next reply: %s' % self.next_reply)

    @staticmethod
    def update_mock_text(text):
        with open('user_tweet_history.txt', 'a') as user_tweet_history_fd:
            user_tweet_history_fd.write("\n")
            user_tweet_history_fd.write(str(text.encode('ascii', 'ignore'), 'utf-8'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--handle',
                        required=True,
                        type=str,
                        dest='followed_handle',
                        action='store',
                        metavar='HANDLE',
                        help='Twitter handle (without @)')
    parser.add_argument('--mock',
                        dest='mock_mode',
                        default=False,
                        action='store_true',
                        help='enable mock mode')
    parser.add_argument('--hashtags',
                        dest='hashtags',
                        default=[],
                        action='append',
                        help='hashtags to append to all replies (may be specified more than once)')
    args = parser.parse_args()
    log.info('started')
    log.debug('args: %s' % args)

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth)

    found_users = api.lookup_users(screen_names=[str(args.followed_handle)])

    if len(found_users) != 1:
        log.error('Lookup for twitter handle %s failed' % args.followed_handle)
        sys.exit()

    followed_user_id = found_users[0].id
    log.debug('followed_user_id: %s' % followed_user_id)

    twitterStream = Stream(auth, Listener(api, followed_user_id, args.followed_handle, args.mock_mode, args.hashtags))
    twitterStream.filter(follow=[str(followed_user_id)], async=True)
