import tweepy
import time
import os
import config
import ocr
import book_api
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
# (extra) Cross reference with other sources for clarity
# ------------------------------------------------------------------------------------------

def main():
  api = setup_api()
  api.update_status # Create stream connection
  
  streamLister = MyStreamListener(api)
  stream = Stream(auth = api.auth, listener = streamLister)
  
  # start stream
  stream.filter(follow = [config.follower]) # Will Change to @WhatBookIsThat


# Should be its own file
class MyStreamListener(StreamListener):

  def __init__(self, api):
    self.api = api
    self.error_replies = ('Hey! Please send me photos with readable text please.',
    'Please do not send me GIFS...',
    'I cannot find any text with picture you gave me. Maybe try another picture please.',
    'I cannot find any results with the text you gave me. Maybe try a different quote.' )

  def on_status(self, status):
    print('-----------------------------------------------')
    # self.reply_back(status) if config.follower == status.in_reply_to_user_id_str else print('Doing nothing please -- return') 
    self.reply_back(status)
    # sleep(5)
    print('-----------------------------------------------')

  def reply_back(self, status):
    asking_user = status.author.name
    tweet = status.text
    print('Author - ' + asking_user)
    print('Tweet - ' + tweet)
    print('=================================')
    if not hasattr(status, 'extended_entities'):
      return print(self.error_replies[0])
    if status.extended_entities['media'][0]['type'] != 'photo':
      return print(self.error_replies[1])
    try:
      pict_txt = ocr.ocr_url(url = status.extended_entities['media'][0]['media_url'])
      if len(pict_txt) > 500:
        pict_txt = pict_txt[:500]
        if '.' in pict_txt:
          pict_txt = pict_txt[: -pict_txt[::-1].find('.')]
      book_searches = book_api.find_quote(pict_txt)
      if (book_searches == 2 or book_searches == 3):
        return print(self.error_replies[book_searches])
      url_link = 'https://amazon.ca/dp/' + book_searches + '/?tag=' + config.amazon_id
      self.api.update_status(url_link) # TODO MUST LIMIT THE CHARACTERS TO 280
      # self.api.update_status('@'+ user_to_reply + " " + url_link)
      # self.api.send_direct_message(status.author.id_str, "Please type direct message here") # Need Direct messages permission
      # print(url_link)
    except tweepy.TweepError as e:
      print("'************ Something Went Wrong ************'")
      print('************' + e.response.text + '************')

  # Might want to look at backoff strategies
  def on_error(self, tweet_code):
    # returning False in on_error disconnects the stream
    # returning non-False reconnects the stream, with backoff.
    if tweet_code == 420: 
      return False
    if tweet_code == 187: #Status is duplicate error
      return True
    if tweet_code == 160: #Already followed error
      return True
    if tweet_code == 139: #Already favorited error
      return True
    if tweet_code == 327: #Already retweeted the same tweet more than once
      return True
    if tweet_code == 226: #Spam error
      return True

# Should be its own file
def setup_api():
  api_key = config.api_key
  api_secret = config.api_secret
  access_token = config.access_token
  token_secret = config.token_secret
  auth = OAuthHandler(api_key, api_secret)
  auth.set_access_token(access_token,token_secret)
  return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if __name__ == '__main__':
  main()

