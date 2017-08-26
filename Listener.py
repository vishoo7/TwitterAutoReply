import random

import markovify
from tweepy import StreamListener

from main import log
from utils import gen_hashtags


class Listener(StreamListener):
    def __init__(self, api, followed_user_id, followed_user_handle, mock_mode, hashtags):
        super().__init__(api)
        self.tweet_data = []
        self.followed_user_id = followed_user_id
        self.followed_user_handle = followed_user_handle

        self.mock_mode = mock_mode
        self.hashtags = hashtags
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

            self.load_next_reply(self.mock_mode, self.hashtags)

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