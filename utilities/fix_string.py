import logging
logger = logging.getLogger('twitter_stream')

'''
Will move OCR string fixing code to this file
'''

def fix_text(text):
  '''
  Cleans text from OCR.
  1.a) Finds first proper sentence (correct grammar, avoids randomly arranged text)
  1.b) If no actually sentence (no uppercase, no punctuation), simply gives the raw text
  2. Shortens text to 300 characters if need be.
  '''
  fixed_text = text

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
  return 'NO_CAPITAL_LETTER'

def find_punctuation(text):
  return 'NO_PUNCTUATION'