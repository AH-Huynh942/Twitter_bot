import logging
logger = logging.getLogger('twitter_stream')

'''
Function to remove nonsense and jargon to improve the text interpretation
--Currently removes:
-WARNING: REMOVES NUMBERS ON REGULAR LINES TOO-the numberring on certain pages (sometimes comes out as single linse with just numbers)
-MUST FIX-removes the excess text found from different pages that sometimes get caught while taking the picture of the intended page0
-Check for improper sentences at the beginning of the string (Must start with upper case and end with period, question mark, exclamation mark semicolon)
-PRIORITY- REMOVE Initial Jargon!!!!!! 
'''


def fix_text(txt):
  short_txt = txt
  if len(short_txt) > 250: # shortens text to 250 characters. removes none finished sentences
    short_txt = short_txt[:250]
    if '.' in short_txt:
      short_txt = short_txt[: -short_txt[::-1].find('.')]
  fixed_txt = ''
  for newline in short_txt: # fix 1
    if not (newline.isdecimal()):
      fixed_txt = fixed_txt + newline
  logger.info('**********************************OCR RAW TEXT**********************************')
  logger.info(fixed_txt)
  logger.info('********************************************************************************')
  return(fixed_txt)

def fix_text2(txt):
  short_txt = txt
  uppercase_int = search_for_uppercase(txt)
  if (len(short_txt) - uppercase_int) > 250: # shortens text to 250 characters. removes none finished sentences
    short_txt = short_txt[uppercase_int:(250+uppercase_int)]
    if '.' in short_txt:
      short_txt = short_txt[: -short_txt[::-1].find('.')]
  fixed_txt = ''
  for newline in short_txt: # fix 1
    if not (newline.isdecimal()):
      fixed_txt = fixed_txt + newline
  return(fixed_txt)

text = "Welcom bd tow fdshaf dsaf. gffdsadafdsf Redafdsafdsalkgh? The worst things in life are the best things!"

def fix_text3(text, tool):
  starting_index = get_first_sentence_char(text,tool)
  if starting_index == -1:
    starting_index = search_for_uppercase(text)
  print(str(starting_index) + " STARTING INDEX PLEASE")
  return text[starting_index:]

def get_first_sentence_char(text, tool):
  if (len(text) == 0):
    return -1 # no viable sentence!
  uppercase_int = search_for_uppercase(text)
  punctuation_int = search_for_punctuation(text)
  first_sentence = text[uppercase_int:punctuation_int] #Complete sentence
  errors = tool.check(first_sentence)
  if (len(errors) == 0):
    return uppercase_int # Start with this sentence (aka the initial integer) 
  else:
    return get_first_sentence_char(text[punctuation_int:],tool)


'''
1.Check for Uppercase letter(search_for_uppercase) to find the start of the first sentence
2. First the first punctuation (question mark, period, exclamation marks)
3. Check if the between upper case and 
 (These check for the first viable sentence and not just jargon on the the start)
4. If above sentence is perceived correct then, start with that sentence. otherwise move on - cut that part out!
'''

def search_for_sentence(text):
  uppercase_int = 0  # if all lowercase
  punctuation_int = len(text)
  uppercase_found = False
  for i in range(len(text)):
    if text[i].isupper() and not uppercase_found:
      uppercase_int = i
      uppercase_found = True
    if text[i] == '!' or text[i] == '?' or text[i] == '.':
      punctuation_int = i + 1
      break
  return (uppercase_int, punctuation_int, text[uppercase_int:punctuation_int])    

def search_for_uppercase(txt):
  uppercase_int = 0  # if all lowercase
  for i in range(len(txt)):
    if txt[i].isupper():
      uppercase_int = i
      break
  return uppercase_int

def search_for_punctuation(txt):
  punctuation_int = len(txt)
  for i in range(len(txt)):
    if txt[i] == '!' or txt[i] == '?' or txt[i] == '.':
      punctuation_int = i + 1
      break
  return punctuation_int