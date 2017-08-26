#!/usr/bin/env python3.5

import argparse
import logging
import sys

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream

from Listener import Listener
from credentials import *

log = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s'))
stdout_handler.setLevel(logging.INFO)
log.addHandler(stdout_handler)
log.setLevel(logging.INFO)

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
