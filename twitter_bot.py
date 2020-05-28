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
# (0) Ask Tim if you want to check for links with the specific quote -- LATER
# (0) Have to limit the picture size (1Mb)
# (0) Have to limit the input text given (string parsing/trucation)
# (0) Improve accuracy of ocr *************** lot of variables
# (0) Improve accuracy of book links *********** lot of variables
# (1) Search (viable Google) for who was the original author of the quote -- IDENTIFY ISBN NUMBER
# (2) Create a url link that links to online merchant using ISBN and Affliate Code
# (extra) Cross reference with other sources for clarity
# (Maybe) Add where he quoted it from
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
    # TODO: Need to check own name 
    # self.name = my_name
    
    # work around for ending with duplicate replies (50 - 100 different replies)
    self.possible_replies = ["Hey, I'm sorry. I didn't get that",
                             "Umm... I'm sorry, I didn't get your reply.",
                             'Please try a different message',
                             "I don't know what you're trying to say, please be more specific",
                             'Huh... I did not get that...',
                             'What is it are you trying to say',
                             'Hmm... The message you sent is hard to interpret',
                             'Try to be more clear on what you message means']

  def on_status(self, status):
    print('-----------------------------------------------')
    self.reply_back(status) if config.follower == status.in_reply_to_user_id_str else print('Doing nothing please -- return') 
    print('-----------------------------------------------')

  def reply_back(self, status):
    user_to_reply = status.author.name
    tweet = status.text
    print('Author - ' + user_to_reply)
    print('Tweet - ' + tweet)
    print('=================================')
    if not hasattr(status, 'extended_entities'):
      return print('Please send me photos with readable text please')
    if status.extended_entities['media'][0]['type'] != 'photo':
      return print('Please do not send me GIFS')
    try:
      picture_text = ocr.ocr_url(url = status.extended_entities['media'][0]['media_url'])
      book_link = book_api.find_quote(picture_text)
      self.api.update_status('@'+ user_to_reply + " " + book_link)
      # self.api.send_direct_message(status.author.id_str, "Please type direct message here") # Need Direct messages permission
      print(book_link)
      sleep(5)
    except tweepy.TweepError as e:
      print("Something Went Wrong")
      print(e.reason)
      sleep(5)

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

