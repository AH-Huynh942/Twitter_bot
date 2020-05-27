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
# Creating a listener object:
# override tweepy.StreamListener to add logic to on_status
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
    author = status.author.name
    tweet = status.text
    reply_to_me = tweet[0:7] #Twit_bot name
    print('-----------------------------------------------')
    print('Author - ' + author)
    print('Tweet - ' + tweet)
    try:
      print('=================================')
      if hasattr(status, 'extended_entities'):
        if status.extended_entities['media'][0]['type'] == 'photo':
          try:
            picture_text = ocr.ocr_url(url = status.extended_entities['media'][0]['media_url'])
            book_link = book_api.find_quote(picture_text)
            print(book_link)
          except:
            print("Something Went Wrong")
          # self.retweet(reply_to_me, book_link)
        else:
          print('Please do not send me GIFS')
      else:
        print('Please send me media objects')
      print('=================================')
    except tweepy.TweepError as e:
        print(e.reason)
        sleep(5)
    print('-----------------------------------------------')

  """
  Have to limit tweets to 120 characters
  """
  # Gives a tweet 
  def tweet(message):
    self.api.update_status(message)

  # tweets back to the given author with the message
  def retweet(author, message):
    self.api.update_status('@' + author + " " + message)

  # Might want to lok at backoff strategies
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

