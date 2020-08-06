import logging
from utilities.setup_logs import setup_loggers

from init_twitter_bot import initiate_twitter_api
from tweepy.streaming import Stream
from twitter_listener import TwitterStreamListener

# logging.disable(logging.DEBUG)

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