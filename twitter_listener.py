import logging
logger = logging.getLogger('twitter_stream')

import json
import tweepy
import config
from utilities.ocr import find_text  
from utilities.string_fix import fix_text
from utilities.book_api import search_for_books
from utilities.url_checker import check_urls
from tweepy.streaming import StreamListener

class TwitterStreamListener(StreamListener):
  """ The twitter bots main functionalities and responses """

  def __init__(self, api, my):
    self.api = api # Twitter API
    self.my = my # Called with api.me()
    self.twitter_ids = {}
    with open('replies.json') as replies:
      self.error_replies = json.load(replies)
      # CURRENT ERROR MESSAGES: no_media, no_photo, no_text_with_pic, no_results_with_pic, 
      # no_media_in_reply, no_photo_in_reply, no_text_with_pic_in_reply, no_results_with_pic_in_reply, encountered_error, multiple_images, no_url
  
  def on_connect(self):
    """Called onced connected to streaming server"""
    logger.info('********************************************************************************')
    logger.info('\n Success! Connection connected to streaming server, awaiting tweets. \n' )
    logger.info('********************************************************************************')
    return

  def on_status(self, status):
    """Called when @mentions toward twitter user or the user's own tweets"""
    logger.info('**********************************ON STATUS*************************************')
    try:
      user_name = status.author.screen_name
      tweet = status.text
      user_id = status.author.id_str

      if user_id not in self.twitter_ids:
        self.twitter_ids[user_id] = {}
        for key in self.error_replies.keys():
          self.twitter_ids[user_id][key] = 0

      # logger.debug(status)
      logger.info(f'Author - {user_name}')
      logger.info(f'Tweet - {tweet}')
      
      tweet_type = self.identify_tweet(status) #function in class
      logger.debug(f"tweet_type = {tweet_type}")      
      
      if (tweet_type == 'MY OWN TWEET') or (tweet_type == 'TWEET REPLY TO ME'):
        if (status.in_reply_to_status_id is not None):
          logger.info(f'Reply to ...{status.in_reply_to_screen_name} in {status.in_reply_to_status_id_str}')
        return

      tweet_to_check = status if (tweet_type == 'TWEET THREAD') else status 
      if not (hasattr(tweet_to_check, 'extended_entities')):
        return self.give_error_reply(user_id, user_name, 'no_media_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_media', tweet_to_check.id)
      elif tweet_to_check.extended_entities['media'][0]['type'] != 'photo': 
        return self.give_error_reply(user_id, user_name, 'no_photo_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_photo', tweet_to_check.id)

      pic_text = find_text(url = tweet_to_check.extended_entities['media'][0]['media_url']) # see utilities.ocr.py - find_text

      if not (pic_text): # MIGHT MAKE IT MORE SOPHISTICATED IN ERROR CHECKING
        return self.give_error_reply(user_id, user_name, 'no_text_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_text_with_pic', tweet_to_check.id)

      fixed_text = fix_text2(pic_text) # See utilitie.string_fix.py - fix_text
      
      books = search_for_books(fixed_text) # See utilities.book_api.py - search_for_books

      if (books == 'NO_TEXT'):
        return self.give_error_reply(user_id, user_name, 'no_text_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_text_with_pic', tweet_to_check.id)
      elif (books == 'NO_RESULTS'):
        return self.give_error_reply(user_id, user_name, 'no_results_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_results_with_pic', tweet_to_check.id)
    
      possible_urls = []
      for isbn in books:
        possible_urls.append('https://www.amazon.ca/dp/'+ isbn)  
      viable_urls = check_urls(possible_urls) # see utilities.url_checker.py - check_urls

      #Extra step -- Scan for related products using the ISBN given (multiple ASIN is prefered)

      if not viable_urls: # LIST IS EMPTY - Should be Amazon links
        return self.give_error_reply(user_id, user_name, 'no_urls', tweet_id)

      # Should be the most relatable book - not one that is available first
      url_link = viable_urls[0] + '/?tag=' + config.amazon_id
      self.api.update_status(f'@{user_name} Here you go, this is an Amazon link for you {url_link}', tweet_to_check.id)
    except tweepy.TweepError as e:
    # see twitter documentation for all twitter status codes - https://developer.twitter.com/en/docs/basics/response-codes
      logger.error('Error handling!')
      logger.error('Error: %s', e.response.text)

  def identify_tweet(self,status):
    '''
    Distinguised what type tweets:
    -The Bot's own tweet
    -Regular tweets that just mention twitter_bot
    -A tweet comment/reply to ANOTHER tweet(the tweet commented upon CONTAINS the image that needs to be looked at)
    -Commenting/Replying on the bot's own tweet -- check in_reply_to_screen == my.screen_name
    '''
    if (status.author.id == self.my.id):
      # logger.debug('My own tweet')
      # logger.debug('Doing nothing')
      return 'MY OWN TWEET'
    elif (status.in_reply_to_status_id is None):
      # logger.debug('Simple mentioned tweet!') 
      # logger.debug('check tweet for photo')
      return 'REGULAR TWEET MENTION'
    elif (status.in_reply_to_user_id == self.my.id):
      # logger.debug('comment on the bots own tweet')
      # logger.debug('Why!? - Do not do anything')
      return 'TWEET REPLY TO ME'
    else:
      # logger.debug('Check the replied status for photo')
      # logger.debug('find tweet via status_id')
      # logger.debug('check that tweet for image')
      return 'TWEET THREAD'

  def give_error_reply(self, user_id, user_name, error_type, tweet_id):
    if self.twitter_ids[user_id][error_type] < len(self.error_replies[error_type]):
      message = '@{}{}'.format(user_name, self.error_replies[error_type][self.twitter_ids[user_id][error_type]])
      self.api.update_status(message, tweet_id)
      self.twitter_ids[user_id][error_type] += 1 
  
  def on_limit(self, track):
    """Called when stream connection times out"""
    logger.warning("*********************************ON TIMEOUT************************************")
    logger.warning(f'track: %s', track)
    logger.warning('*******************************************************************************')
    time.sleep(10*60)    
    return True

  def on_warning(self, notice):
    """Called when a disconnection warning message arrives"""
    logger.warning("*********************************ON WARNING************************************")
    logger.warning(f'notice: %s', notice)
    logger.warning('*******************************************************************************')
    time.sleep(10*60)    
    return True

  def on_disconnect(self, notice):
    """Called when twitter sends a disconnect notice"""
    logger.error("*********************************ON DISCONNECT************************************")
    logger.error(f'notice: %s', notice) # Add to database erro
    logger.error('**********************************************************************************')
    time.sleep(10*60)    
    return True

  def on_error(self, tweet_code):
    """Called when a non-200 status code is returned"""
    logger.error("*********************************ON ERROR*****************************************")
    logger.error(f'tweet_code: %s', tweet_code)
    logger.error('**********************************************************************************')
    time.sleep(10*60)    
    return # Aborts stream disconnection
  
  def on_timeout(self, notice):
    logger.warning("*********************************ON TIMEOUT************************************")
    logger.warning(f'notice: %s', notice)
    logger.warning('*******************************************************************************')
    time.sleep(10*60)    
    return True