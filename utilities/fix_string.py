import logging
logger = logging.getLogger('twitter_stream')

import re

'''
Will move OCR string fixing code to this file
'''

def clean_text(text):
  '''
  Cleans text from OCR.
  '''
  '''
  Given a string of text -- must figure out what to do with some rubbish like page numbers, jibberish at the beginning, shorten to an acceptable amount
  
  1- Remove jibberish:
    1.a) Finds first proper sentence (correct grammar, avoids randomly arranged text)
    1.b) If no actually sentence (no uppercase, no punctuation), simply gives the raw text
  
  2- Remove page numbers:

  3- Shortens text to 300 characters if need be:
  '''
  # starting_sentence_int = find_capital_letter(text)
  # if(starting_sentence_int == 'NO_CAPITAL_LETTER'):
  #   return fixed_text
  
  # ending_punctuation_int = find_punctuation(text)
  # if(ending_punctuation_int = 'NO_PUNCTUATION'):
  #   return fixed_text

  # MUST BE A WAY TO CHECK IF A STRING CONTAINS A SENTENCE! MUST LOOK UP

  logger.debug('**********************************OCR RAW TEXT**********************************')
  logger.debug(fixed_txt)
  logger.debug('********************************************************************************')
  return(fixed_text)

def find_capital_letter(text):
  for i in range(len(text)):
    if text[i].isupper():
      return(i)
  return 'NO_CAPITAL_LETTER'

def find_punctuation(text):
  for i in range(len(text)):
    if text[i] == '!' or text[i] == '?' or text[i] == '.':
      return(i)
  return 'NO_PUNCTUATION'


def find_sentence(text):
  find = '/(^.*?[a-z]{2,}[.!?])\s+\W*[A-Z]/'
  # regex = re.search(find, text)
  regex = re.match(find, text)
  return regex

test = 'gfdagfdsgfdhgfhgfdshgsgrestr3et43 vfshfgdshgfdgfsd ?vcdbvds bgfvs cvbvs?safdagfdsfdsgfd'
test2 = 'What is the final question?'
print(find_sentence(test))
print(find_sentence(test2))