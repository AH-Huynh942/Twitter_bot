import requests

# from config import google_key

def find_quote(q, maxResults = 3, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    if 'totalItems' not in r.json():
        # print('There is no totalItems')
        return 2
    if (r.json()['totalItems'] <= 0):
        # print('TotalItems is less than 0')
        return 3
    if (len(r.json()['items'][0]['volumeInfo']['industryIdentifiers']) > 1):
        return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    else:
        return 3

def quote(q, maxResults = 3, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    if 'totalItems' not in r.json():
        # print('There is no totalItems')
        return 2
    if (r.json()['totalItems'] <= 0):
        # print('TotalItems is less than 0')
        return 3
    if (len(r.json()['items'][0]['volumeInfo']['industryIdentifiers']) > 1):
        print("**************Book Info Given***************\n")
        print(r.json())
        print('\n')
        print("**************Book Info Given***************\n")
        return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    else:
        return 3