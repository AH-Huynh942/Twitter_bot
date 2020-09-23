import logging
from utilities.setup_logs import setup_loggers

import config

from tweepy.api import API
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream
from twitter_listener import TwitterStreamListener

# logging.disable(logging.DEBUG)

def initiate_authentication():
    """ Creates authentication with credential keys from config.py file """
    api_key = config.api_key
    api_secret = config.api_secret
    access_token = config.access_token
    token_secret = config.token_secret
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token,token_secret)
    # logger.info(f'Authenitication key: {auth}')
    return auth

def initiate_twitter_api():
    """ Creates and setups the twitter api via with Tweepy (see Tweepy doc) """
    auth = initiate_authentication()
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # logger.info(f'Tweepy API: {api}')
    return api

def main():
    api = initiate_twitter_api() # Create tweepy api - see init_twitter_bot.py
    auth_user = api.me() # Authenticated User Object - id, id_str, screen_name, etc...
    logger.info(auth_user)

    stream_listener = TwitterStreamListener(api, auth_user) # See twitter_listener for the main functionality of the bot
    stream = Stream(auth = api.auth, listener=stream_listener)

    # starts stream - follows the assigned twitter-id AND tracks any @mentions
    stream.filter(follow = [auth_user.id_str], track = [auth_user.screen_name])

if __name__ == "__main__":
    setup_loggers()
    logger = logging.getLogger('main')
    main()