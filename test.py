# import env
import os
from decouple import config

print(config('TWITTER_API_KEY'))
print(config('TWITTER_API_SECRET_KEY'))
print(config('TWITTER_API_TOKEN_ACCESS'))
print(config('TWITTER_API_TOKEN_SECRET'))
print(config('AMAZON_ID'))
print(config('TWITTER_ID'))
print(config('OCR_API_KEY'))
print(config('GOOGLE_KEY'))