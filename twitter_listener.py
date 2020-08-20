import logging
logger = logging.getLogger('twitter_stream')

import json
import time
import tweepy
import config
from utilities.ocr import find_text  
from utilities.string_fix import fix_text2
from utilities.book_api import search_for_books
from utilities.url_checker import check_urls
from tweepy.streaming import StreamListener

# TODO: Extra step (7.5) -- Scan for related products using the ISBN given (multiple ASIN is prefered)
# TODO: Return and self.error_reply function in one line
# TODO: Prevent more than 5 concurrent connections to OCR api

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
            
            # Step 1. Check for tweet type(s) - (tweet reply to me, my own tweet, tweet thread, regular tweet)
            tweet_type = self.identify_tweet(status) # function in class
            logger.debug(f"tweet_type = {tweet_type}")      
            
            # Step 2. Checks for tweet type being a direct tweet/my own toward bot - give no reply (otherwise cause endless loop)
            if (tweet_type == 'MY OWN TWEET') or (tweet_type == 'TWEET REPLY TO ME'):
                if (status.in_reply_to_status_id is not None):
                    logger.info(f'Reply to ...{status.in_reply_to_screen_name} in {status.in_reply_to_status_id_str}')
                return

            tweet_to_check = self.api.get_status(status.in_reply_to_status_id) if (tweet_type == 'TWEET THREAD') else status
            # Step 3. Checks for presence of viable image (no gifs and only the first image is used)
            if not (hasattr(tweet_to_check, 'extended_entities')):
                self.give_error_reply(user_id, user_name, 'no_media_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_media', status.id)
                return 
            elif tweet_to_check.extended_entities['media'][0]['type'] != 'photo': 
                self.give_error_reply(user_id, user_name, 'no_photo_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_photo', status.id)
                return 

            # Step 4. Finds text within image 
            pic_text = find_text(url = tweet_to_check.extended_entities['media'][0]['media_url']) # see utilities.ocr.py - find_text
            # Step 4.5. Reply error with no text in picture
            if not(isinstance(pic_text, str)):
                if (pic_text['ErrorMessage'] == 'No text'):
                    self.give_error_reply(user_id, user_name, 'no_text_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_text_with_pic', status.id)
                    return 
                else:
                    self.give_error_reply(user_id, user_name, 'encountered_error', status.id)
                    return 

            # Step 5. Cleans/Clearifies the text that was interpreted giving a better result in book search
            fixed_text = fix_text2(pic_text) # See utilitie.string_fix.py - fix_text
            
            # Step 6. Finds books with the fixed text
            books = search_for_books(fixed_text) # See utilities.book_api.py - search_for_books

            # Step 6.5. Reply error with no results found
            if (books == 'NO TEXT'):
                logger.info('ENCOUNTERED ERROR - STEP 6.5 - NO TEXT')
                self.give_error_reply(user_id, user_name, 'no_text_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_text_with_pic', status.id)
                return 
            elif (books == 'NO RESULTS'):
                logger.info('ENCOUNTERED ERROR - STEP 6.5 - NO RESULTS')
                self.give_error_reply(user_id, user_name, 'no_results_with_pic_in_reply' if (tweet_type == 'TWEET THREAD') else 'no_results_with_pic', status.id)
                return 

            # Step 7 Version 2: Get title of most relevant book and author
            book_title = books[0]['title'] # title of first result in book searchs
            author_title = '' # author of first result in book searchs
            for i, author in enumerate(books[0]['authors']):
                if (i == len(books[0]['authors'])-1 and len(books[0]['authors']) == 1):
                    author_title = ' ' + author
                    break
                if (i == len(books[0]['authors'])-1):
                    author_title = author_title + ' and ' + author
                    break
                author_title = author_title + ' ' + author + ','
            # Step 7. Searches for viable amazon links to give out
            # possible_urls = []
            # for isbn in books:
            #     possible_urls.append('https://www.amazon.ca/dp/'+ isbn)  
            # viable_urls = check_urls(possible_urls) # see utilities.url_checker.py - check_urls
            
            # Step 7.5. Reply error when there is no amazon links found
            # if not viable_urls:
            #     logger.info('ENCOUNTERED ERROR - STEP 7.5')
            #     self.give_error_reply(user_id, user_name, 'no_urls', status.id)
            #     return 

            # Step 8. Tweet back to person with amazon link of the related book
            # url_link = viable_urls[0] + '/?tag=' + config.amazon_id
            # self.api.update_status(f'@{user_name} Here you go, this is an Amazon link for you {url_link}', status.id) -- must add back later

            # Step 8 Version 2: Tweet back to person with the title and author of the related book
            # self.api.update_status(f'@{user_name} Here you go, the title of the book is "{book_title}" and the the Author is {author_title}', status.id)
            self.api.update_status(f'@{user_name} Here you go, the title of the book is “{book_title}” by Author{author_title}', status.id)
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
            return 'REGULAR TWEET'
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