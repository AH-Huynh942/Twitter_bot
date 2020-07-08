import tweepy
import time
import os
import config
import ocr
import book_api
import stringfix
import requests
import language_tool_python

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
    self.twitter_ids = {}
    self.no_media_replies = (' You did not tweet me an image. Next time, give me photos with readable text please.',
    ' Once again, you did not give me an image to interpret. Please send me a picture of the book your quoting.',
    ' I am getting tired of reminding you to tweet me images... Please give me a graphic, preferable with some writing.',
    ' I am tired of reminding you... This is an automatic message - 1',
    ' I am tired of reminding you... This is an automatic message - 2',
    ' I am tired of reminding you... This is an automatic message - 3',
    ' I am tired of reminding you... This is an automatic message - 4',
    ' I am tired of reminding you... This is an automatic message - 5',)
    self.not_photo_replies = (' Please do not send me GIFS, images instead would be great!',
    ' I do not read other media, I only read photos please.',
    ' Huh, that does not look like an image to me... I reminded you right?',
    ' Okay, stop it. this is just going to be an automated message now... - 1',
    ' Okay, stop it. this is just going to be an automated message now... - 2',
    ' Okay, stop it. this is just going to be an automated message now... - 3',
    ' Okay, stop it. this is just going to be an automated message now... - 4',
    ' Okay, stop it. this is just going to be an automated message now... - 5',)
    self.no_text_with_pic_replies = (' I did not find any text in the image you sent me - ', ' Huh, still no text found, that is odd')
    self.no_results_with_pic_replies = (' I did get any results in the text you sent me - ', ' I could not get any results for some reason, maybe send another pic')
    self.encountered_error_replies = (' The file type seems to not be correct - ', ' Sorry there must be congestion with the OCR - ', ' Huh, the photo does not be a ledgeable format - ')
    # self.tool = language_tool_python.LanguageTool('en-US')
    
    # self.error_replies = ('Hey! Please send me photos with readable text please.',
    # 'Please do not send me GIFS...',
    # 'I cannot find any text with the picture you gave me. Maybe try another picture please.',
    # 'I cannot find any results with the text you gave me. Maybe try a different quote please.' )

  def on_connect(self):
    """Called once connected to streaming server"""
    print('-----------------------------------------------')
    print("\n Success! Connection connected to streaming server \n ")
    print('-----------------------------------------------')

  def on_status(self, status):
    print('----------------ON STATUS--------------------')
    if config.follower == status.user.id_str: 
      print('OWN TWEET - MOST LIKELY REPLYING BACK')
      print(status.created_at) # Date
      print('Author - ' + status.user.screen_name)
      print('Tweet - ' + status.text)
      print('Tweet link - ' + status.id_str) 
    elif config.follower == status.in_reply_to_user_id_str:
      self.reply_back(status) 
    else:
      print('OTHER TYPE OF TWEET')
      print(status)
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
    print(status.created_at)
    print('Author - ' + user_name)
    print('Tweet - ' + tweet)
    print('Tweet link -' + status.id_str)
    print('=================================')
    if not user_id in self.twitter_ids:
      self.twitter_ids[user_id] = {}
    if not hasattr(status, 'extended_entities'):
      if 'no_media_reply' in self.twitter_ids[user_id]:
        self.twitter_ids[user_id]['no_media_reply'] = self.twitter_ids[user_id]['no_media_reply'] + 1
        if self.twitter_ids[user_id]['no_media_reply'] > 5:
          return
      else:
        self.twitter_ids[user_id]['no_media_reply'] = 0
      print (self.twitter_ids[user_id]['no_media_reply'])
      self.api.update_status("@" + user_name + self.no_media_replies[self.twitter_ids[user_id]['no_media_reply']])
      return
    if status.extended_entities['media'][0]['type'] != 'photo':
      if 'not_photo_reply' in self.twitter_ids[user_id]:
        self.twitter_ids[user_id]['not_photo_reply'] = self.twitter_ids[user_id]['not_photo_reply'] + 1
        if self.twitter_ids[user_id]['not_photo_reply'] > 5:
          return
      else:
        self.twitter_ids[user_id]['not_photo_reply'] = 0
      print (self.twitter_ids[user_id]['not_photo_reply'])
      self.api.update_status("@" + user_name + self.not_photo_replies[self.twitter_ids[user_id]['not_photo_reply']])
      return
    try:
      fixed_txt = ''

      pict_txt = ocr.ocr_url(url = status.extended_entities['media'][0]['media_url']) # see ocr.py

      if isinstance(pict_txt, int):
        if 'encountered_err' in self.twitter_ids[user_id]:
          self.twitter_ids[user_id]['encountered_err'] = self.twitter_ids[user_id]['encountered_err'] + 1
        else:
          self.twitter_ids[user_id]['encountered_err'] = 0
        print(self.twitter_ids[user_id]['encountered_err'])
        self.api.update_status("@" + user_name + self.encountered_error_replies[pict_txt] + str(self.twitter_ids[user_id]['encountered_err']))
        return
      print("**************UNFIXED TEXT***************")
      print(pict_txt)
      print("**************UNFIXED TEXT***************")

      fixed_txt = stringfix.fix_text(pict_txt) # see stringfix.py
      print("****************FIXED TEXT***************")
      print(fixed_txt)
      print("****************FIXED TEXT***************")
  
      book_searches = book_api.find_quote(fixed_txt) # see book_api.py
      print(book_searches)
      
      if book_searches == 'NO TEXT':
        if 'no_text_with_pic_reply' in self.twitter_ids[user_id]:
          self.twitter_ids[user_id]['no_text_with_pic_reply'] = self.twitter_ids[user_id]['no_text_with_pic_reply'] + 1
        else:
          self.twitter_ids[user_id]['no_text_with_pic_reply'] = 0
        print(self.twitter_ids[user_id]['no_text_with_pic_reply'])
        self.api.update_status('@' + user_name + self.no_text_with_pic_replies[0] + str(self.twitter_ids[user_id]['no_text_with_pic_reply']))
        return
      elif book_searches == 'NO RESULTS':
        if 'no_results_with_pic_reply' in self.twitter_ids[user_id]:
          self.twitter_ids[user_id]['no_results_with_pic_reply'] = self.twitter_ids[user_id]['no_results_with_pic_reply'] + 1
          return
        else:
          self.twitter_ids[user_id]['no_results_with_pic_reply'] = 0
        print(self.twitter_ids[user_id]['no_results_with_pic_reply'])
        self.api.update_status('@' + user_name + self.no_results_with_pic_replies[0] + str(self.twitter_ids[user_id]['no_results_with_pic_reply']))
        return
      # if (book_searches == 2 or book_searches == 3):
      #   if 'not_photo_replies' in self.twitter_ids[user_id]:
      #     else:
      #     self.twitter_ids[user_id]['not_photo_replies'] = 0
      # return self.api.send_direct_message(user_id,(self.error_replies[book_searches]))
      
      #Extra step -- Scan for related products using the ISBN given (multiple ASIN is prefered)      
      
      url_link =  'https://amazon.ca/dp/' + book_searches + '/?tag=' + config.amazon_id
      
      self.api.update_status('@'+ user_name + " Here you go, this is an Amazon link for you " + url_link) # TODO MUST LIMIT THE CHARACTERS TO 280
      print('=================================')
    except tweepy.TweepError as e:
      print("'************ Something Went Wrong ************'")
      print(e.response)

  def on_limit(self, track):
    """Called when stream connection times out"""
    print("----------------- ON TIMEOUT ---------------------")
    print(track)
    print("----------------- ON TIMEOUT ---------------------")
    time.sleep(10 * 60)    
    return True


  def on_warning(self, notice):
    """Called when a disconnection warning message arrives"""
    print("----------------- ON WARNING ---------------------")
    print(notice)
    print("----------------- ON WARNING ---------------------")
    time.sleep(10 * 60)    
    return True

  def on_disconnect(self, notice):
    """Called when twitter sends a disconnect notice"""
    print("----------------- ON DISCONNECT -------------------")
    print (notice) # Add to database erro
    print("----------------- ON DISCONNECT -------------------")
    time.sleep(10 * 60)    
    return True

  def on_error(self, tweet_code):
    """Called when a non-200 status code is returned"""
    print("----------------- ON ERROR ---------------------")
    print(tweet_code)
    print("----------------- ON ERROR ---------------------")
    time.sleep(10 * 60)    
    return True # Aborts stream disconnection
  
  def on_timeout(self, notice):
    print("----------------- ON TIMEOUT ---------------------")
    print(notice)
    print("----------------- ON TIMEOUT ---------------------")
    time.sleep(10 * 60)    
    return True
    # return True # Aborts stream disconnection

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
