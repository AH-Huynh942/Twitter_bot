import requests

# from config import google_key

def find_quote(q, maxResults = 1, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    # return r.content.decode()
    return r.json()['items'][0]['selfLink']

