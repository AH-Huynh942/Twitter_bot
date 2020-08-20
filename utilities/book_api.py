import logging
logger = logging.getLogger('twitter_stream')

import requests
import goodreads_api_client as GR
from config import google_key, goodreads_key, goodreads_secret

# TESTING FUNCTION - for files
def find_book(q, maxResults = 6, projection = 'full',):
    ''' Searches for books using the google books REST api with search query "q" '''
    printType = 'books'
    url = f'https://www.googleapis.com/books/v1/volumes?q={q}&printType={printType}&maxResults={maxResults}&projection={projection}'

    r = requests.get(url)
    results = r.json()

    logger.debug('*****************************Book Info Given************************************')
    if 'totalItems' not in results:
        logger.debug('There is no totalItems. An empty string was probably given')
        return 'NO TEXT'
    if (results['totalItems'] <= 0):
        logger.debug('TotalItems is zero. Most likely no search results where found')
        return 'NO RESULTS'

    book_isbn = []
    for book in results['items']:
        info = book['volumeInfo']
        book_isbn.append(str(info['industryIdentifiers']))

        if 'selfLink' in book:	logger.debug(f'selfLink - %s', book['selfLink'])
        if 'title' in info:	logger.debug(f'Title - %s', info['title'])
        if 'subtitle' in info:	logger.debug(f'Subtitle - %s', info['subtitle'])
        if 'authors' in info:	logger.debug(f'Author(s) - %s', info['authors']) 
        if 'publisher' in info:	logger.debug(f'Publisher - %s', info['publisher'])
        if 'publishDate' in info:	logger.debug(f'Published date - %s', info['publishDate'])
        if 'description' in info:	logger.debug(f'Desc - %s', info['description'])
        if 'industryIdentifiers' in info:	logger.debug(f'ISBN - %s', info['industryIdentifiers'])
    logger.debug(book_isbn)
    logger.debug('*****************************Book Info Given************************************')
    return book_isbn # NEW WAY OF RETURNING MULTIPLE ISBNs

# REAL FUNCTION
def search_for_books(q, maxResults = 6, projection = 'full',  ):
    '''
    Searches for books using the google books REST api with search query "q" 
    '''
    printType = 'books'
    url = f'https://www.googleapis.com/books/v1/volumes?q={q}&printType={printType}&maxResults={maxResults}&projection={projection}'

    r = requests.get(url)
    results = r.json()

    logger.info('Book Info Given--------------------------------------------------')
    if 'totalItems' not in results: # print('There is no totalItems')
        return 'NO TEXT'
    if (results['totalItems'] <= 0): # print('TotalItems is less than 0')
        return 'NO RESULTS'

    books = []
    for book in results['items']:
        book_id = {'title': "", 'authors': "", 'isbns': {'ISBN_13': "", 'ISBN_10': ""}}
        info = book['volumeInfo']
        if 'selfLink' in book:	logger.info(f'selfLink - %s', book['selfLink'])
        if 'title' in info:
            logger.info(f'Title - %s', info['title'])
            book_id['title'] = info['title']
        # if 'subtitle' in info:	logger.debug(f'Subtitle - %s', info['subtitle'])
        if 'authors' in info:
            logger.info(f'Author(s) - %s', info['authors']) 
            book_id['authors'] = info['authors']
        # if 'publisher' in info:	logger.debug(f'Publisher - %s', info['publisher'])
        # if 'publishDate' in info:	logger.debug(f'Published date - %s', info['publishDate'])
        # if 'description' in info:	logger.debug(f'Desc - %s', info['description'])
        if 'industryIdentifiers' in info:	
            logger.info(f'ISBN - %s', info['industryIdentifiers'])
            for isbn in info['industryIdentifiers']:
                if isbn['type'] == 'ISBN_13':
                    book_id['isbns']['ISBN_13'] = isbn['identifier']
                if isbn['type'] == 'ISBN_10':
                    book_id['isbns']['ISBN_10'] = isbn['identifier']
        books.append(book_id)
    return books

def find_purchasable_books(text):
    '''
    GoodReads API finding viable Amazon links (that works)
    '''
    client = GR.Client(developer_key = goodreads_key, developer_secret = goodreads_secret)
    book = client.Book.title('Harry Potter')
    # book = client.search_book('Chronicles of Prydain', 'title',1)
    keys_wanted = ['id', 'title', 'isbn']
    reduced_book = {k:v for k, v in book.items() if k in keys_wanted}
    print(reduced_book)
    print(book)

    # searchTitle = 'title'
    # url = f'https://www.goodreads.com/search.xml?key={goodreads_key}&q={q}&page={1}&search={searchTitle}'
    # response = requests.get(url)
    # tree = ElementTree.fromstring(response.content)
    # print(tree.find('search'))
    # except:
    #   pass