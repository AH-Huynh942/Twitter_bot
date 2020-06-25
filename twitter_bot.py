import tweepy
import time
import os
import config
import ocr
import book_api
import stringfix
import requests

from tweepy.auth import OAuthHandler
from tweepy.api import API
from tweepy.streaming import Stream, StreamListener
# ------------------------------------------------------------------------------------------
# Coded by: Andy Huynh
# Date: April 27, 2020 
# 
# Main Function: Respond to #FigureOutWhereThisQuoteIsFrom
# TODO:
# (extra) Cross reference with other sources for clarity i.e Open Library API, ISBNdb API
# (extra) Add: Oxford dictionary api, Quotes REST api (They Said So Quotes API), Literature Online API 
# (extra) Add: ISBNdb api, SearchItems api, 
# (0) Still need to buy improve on the ocr text interpretation
# (1) No matter what quote from a book, should always get a reliable amazon link.
# TODO: ADD MORE PROGRAMMING ASSURANCES
# TODO: Make a list of wanted statistics data, --> write to database library.
# Tweepy: Streamlistener Object Doc: https://github.com/tweepy/tweepy/blob/78d2883a922fa5232e8cdfab0c272c24b8ce37c4/tweepy/streaming.py
# ------------------------------------------------------------------------------------------

def main():
  api = setup_api()
  api.update_status # Create stream connection
  
  streamLister = MyStreamListener(api)
  stream = Stream(auth = api.auth, listener = streamLister)
  
  # start stream
  stream.filter(follow = [config.follower]) # Will Change to @WhatBookIsThat


class MyStreamListener(StreamListener):

  def __init__(self, api):
    self.api = api
    self.error_replies = ('Hey! Please send me photos with readable text please.',
    'Please do not send me GIFS...',
    'I cannot find any text with the picture you gave me. Maybe try another picture please.',
    'I cannot find any results with the text you gave me. Maybe try a different quote please.' )

  def on_connect(self):
    """Called once connected to streaming server"""
    print('-----------------------------------------------')
    print("\n Success! Connection connected to streaming server \n ")
    print('-----------------------------------------------')

  def on_status(self, status):
    print('-----------------------------------------------')
    # self.reply_back(status) if config.follower == status.in_reply_to_user_id_str else print('Replying...') 
    print("\n On_status \n")
    print('-----------------------------------------------')

  def reply_back(self, status):
    """
    STATISTICS THAT NEED TO BE LOGGED:
    
    DATE & TIME OF TWEET,
    AUTHOR OF TWEET,
    TWEET TEXT,
    TWEET LINK,
    AUTHOR OF BOOK,
    TITLE OF BOOK,
    ISBN (RESULT),
    AMAZON LINK,
    RESULT LINK (FROM GOOGLE BOOKS),
    NUMBER OF RESULTS FOUND,
    WHATISTHATBOOK REPLY CODE,

    IF ERROR -- LOG THE ERROR!

    extra:
    results of the 2nd and 3rd most relevant result
    """

    user_name = status.user.screen_name
    tweet = status.text
    user_id = status.user.id_str
    print('Author - ' + user_name)
    print('Tweet - ' + tweet)
    print('=================================')
    if not hasattr(status, 'extended_entities'):
      return self.api.send_direct_message(user_id, (self.error_replies[0]))
    if status.extended_entities['media'][0]['type'] != 'photo':
      return self.api.send_direct_message(user_id, (self.error_replies[1]))
    try:
      fixed_txt = ''
      pict_txt = ocr.ocr_url(url = status.extended_entities['media'][0]['media_url'])
      fixed_txt = stringfix.fix_text(pict_txt)
      print(fixed_txt)
      book_searches = book_api.find_quote(fixed_txt)
      print(book_searches)
      if (book_searches == 2 or book_searches == 3):
        return self.api.send_direct_message(user_id,(self.error_replies[book_searches]))
      
      #Extra step -- Scan for related products using the ISBN given (multiple ASIN is prefered)      
      
      url_link =  'https://amazon.ca/dp/' + book_searches + '/?tag=' + config.amazon_id
      
      self.api.update_status('@'+ user_name + " " + url_link) # TODO MUST LIMIT THE CHARACTERS TO 280
      self.api.send_direct_message(user_id, "Is this the book your looking for? - " + url_link) # Need Direct messages permission
      print('=================================')
    except tweepy.TweepError as e:
      print("'************ Something Went Wrong ************'")
      print('************' + e.response.text + '************')

  def on_limit(self, track):
    """Called when stream connection times out"""
    print("----------------- ON TIMEOU ---------------------")
    print(track)
    print("----------------- ON TIMEOU ---------------------")

  def on_warning(self, notice):
    """Called when a disconnection warning message arrives"""
    print("----------------- ON WARNING ---------------------")
    print(notice)
    print("----------------- ON WARNING ---------------------")

  def on_disconnect(self, notice):
    """Called when twitter sends a disconnect notice"""
    print("----------------- ON DISCONNECT -------------------")
    print (notice) # Add to database erro
    print("----------------- ON DISCONNECT -------------------")

  def on_error(self, tweet_code):
    """Called when a non-200 status code is returned"""
    print("----------------- ON ERROR ---------------------")
    print(tweet_code)
    print("----------------- ON ERROR ---------------------")

def setup_api():
  api_key = config.api_key
  api_secret = config.api_secret
  access_token = config.access_token
  token_secret = config.token_secret
  auth = OAuthHandler(api_key, api_secret)
  auth.set_access_token(access_token,token_secret)
  # TODO: callback function with connection
  return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if __name__ == '__main__':
  main()
