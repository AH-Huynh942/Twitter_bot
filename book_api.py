import requests

# from config import google_key

def find_quote(q, maxResults = 1, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    if 'totalItems' not in r.json():
        # print('There is no totalItems')
        return 2
    if (r.json()['totalItems'] <= 0):
        # print('TotalItems is less than 0')
        return 3
    return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
