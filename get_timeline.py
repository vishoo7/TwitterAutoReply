#!/usr/bin/env python3.5
# encoding: utf-8

import tweepy
import argparse
import re
import html
from itertools import chain

from credentials import *


def get_all_tweets(screen_name, output_file, filtered_entity_types, filtered_words):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # grab tweets until there are no tweets left to grab
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_tweets.extend(new_tweets)
    oldest_tweet_id = all_tweets[-1].id - 1

    while len(new_tweets) > 0:
        print('getting tweets before %s' % oldest_tweet_id)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_tweet_id)
        all_tweets.extend(new_tweets)
        oldest_tweet_id = all_tweets[-1].id - 1
        print('...%s tweets downloaded so far' % len(all_tweets))

    # filter entities and/or words from tweets
    result = []
    for text, entities in ((t.text, t.entities) for t in all_tweets):
        filtered_entities = []

        for entity_type in filtered_entity_types:
            if entity_type == 'urls':
                filtered_entities.extend(e["url"] for e in entities["urls"])
            elif entity_type == 'user_mentions':
                filtered_entities.extend("@" + e["screen_name"] for e in entities["user_mentions"])
            elif entity_type == 'media':
                if 'media' in entities:
                    filtered_entities.extend(e["url"] for e in entities["media"])

        for thing_to_filter in chain(filtered_entities, filtered_words):
            text = re.sub(str(thing_to_filter), '', text, flags=re.IGNORECASE)

        # clean up retweets if we're filtering out user mentions
        if 'user_mentions' in filtered_entity_types:
            text = re.sub(r'^RT : ', '', text)

        # unescape ampersand
        text = html.unescape(text)

        # remove non-ascii
        text = ''.join(c for c in text if ord(c) < 128)

        result.append(text)

    with open(output_file, 'w') as output_fd:
        for tweet in result:
            if tweet.strip():
                output_fd.write("%s\n" % tweet.strip())

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--handle',
                        required=True,
                        dest='handle',
                        action='store',
                        help='Twitter handle (without @) to fetch timeline for')
    parser.add_argument('--file',
                        required=True,
                        dest='file',
                        default=False,
                        action='store',
                        metavar='FILENAME',
                        help='file to store timeline entries to')
    parser.add_argument('--filter',
                        dest='filtered_words',
                        default=[],
                        action='append',
                        metavar='WORD',
                        help='word to filter from timeline (case insensitive), may specify multiple times')
    parser.add_argument('--exclude-entities',
                        dest='filtered_entities',
                        default=[],
                        choices=['urls', 'user_mentions', 'hashtags', 'media', 'all'],
                        action='append',
                        help='entity type to filter from timeline')
    args = parser.parse_args()
    if args.filtered_entities == 'all':
        args.filtered_entities = ['urls', 'user_mentions', 'hashtags', 'symbols', 'media']

    get_all_tweets(screen_name=args.handle,
                   output_file=args.file,
                   filtered_words=args.filtered_words,
                   filtered_entity_types=args.filtered_entities)
