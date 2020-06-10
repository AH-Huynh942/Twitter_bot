# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import  requests
import json
import config


def find_oxford_quote(word):
  app_id = config.oxford_id
  app_key = config.oxford_key
  # language = 'en'
  word_id = word
  url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/en/'  + word_id.lower()
  #url Normalized frequency
  # urlFR = 'https://od-api.oxforddictionaries.com:443/api/v2/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
  
  r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
  return r.

# print("code {}\n".format(r.status_code))
# print("text \n" + r.text)
# print("json \n" + json.dumps(r.json())) 
