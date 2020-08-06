import logging
logger = logging.getLogger('main')

import config
from tweepy.api import API
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream
from twitter_listener import TwitterStreamListener

'''
DO NOT Start with this file - start with twitter_bot.py
'''

def initiate_authentication():
    """ Creates authentication with credential keys from config.py file """
    api_key = config.api_key
    api_secret = config.api_secret
    access_token = config.access_token
    token_secret = config.token_secret
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token,token_secret)
    logger.info(f'Authenitication key: {auth}')
    return auth

def initiate_twitter_api():
    """ Creates and setups the twitter api via with Tweepy (see Tweepy doc) """
    auth = initiate_authentication()
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    logger.info(f'Tweepy API: {api}')
    return api