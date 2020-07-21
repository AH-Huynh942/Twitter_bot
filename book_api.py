import requests

# from config import google_key

def find_quote(q, maxResults = 6, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    results = r.json()
    if 'totalItems' not in results: # print('There is no totalItems')
        return 'NO TEXT'
    if (results['totalItems'] <= 0): # print('TotalItems is less than 0')
        return 'NO RESULTS'
    book_isbn = []
    print("**************Book Info Given***************")
    for book in results['items']:
        info = book['volumeInfo']
        # selfLink, title, subtitle, authors, isbn = ''
        # if 'selfLink' in book:
        #     print('selfLink = ' + str(book['selfLink']))
        if 'title' in info:            
            print('Title - ' + str(info['title']))
        # if 'subtitle' in info:            
        #     print('Subtitle - ' + str(info['subtitle']))
        # if 'authors' in info:            
        #     print('Author(s) - ' + str(info['authors']))
        if 'industryIdentifiers' in info:
            # print('ISBN - ' + str(info['industryIdentifiers']))
            for isbn in info['industryIdentifiers']:
                # print(isbn)
                if isbn['type'] == 'ISBN_13' or isbn['type'] == 'ISBN_10':
                    book_isbn.append(isbn['identifier'])
        # print('\n')
    print("**************Book Info Given***************")
    return book_isbn

# TEST Func
def quote(q, maxResults = 5, projection = 'full',  ):
    printType = 'books'
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType={}&maxResults={}&projection={}'.format(q, printType, maxResults, projection)
    r = requests.get(url)
    results = r.json()
    if 'totalItems' not in results:
        # print('There is no totalItems')
        return 'NO TEXT'
    if (results['totalItems'] <= 0):
        # print('TotalItems is less than 0')
        return 'NO RESULTS'
    
    book_isbn = []
    print("**************Book Info Given***************")
    for book in results['items']:
        info = book['volumeInfo']
        book_isbn.append(str(info['industryIdentifiers']))

        print('selfLink = ' + str(book['selfLink']))
        print('Title - ' + str(info['title']))
        # print('Subtitle - ' + str(info['subtitle']))
        print('Author(s) - ' + str(info['authors']))
        # print('Publisher - ' + str(info['publisher']))
        # print('Published date - ' + str(info['publishedDate']))
        # print('Desc - ' + str(info['description']))
        print('ISBN - ' + str(info['industryIdentifiers']))
        print('\n')
    print("**************Book Info Given***************")
    return book_isbn # NEW WAY OF RETURNING MULTIPLE ISBNs

    # for isbn in book_isbn:
        # isbn[0]['identifier'] --This is ISBN_13
        # isbn[1]['identifier'] --This is ISBN_10
        # return only the isbn_10
    # if (len(r.json()['items'][0]['volumeInfo']['industryIdentifiers']) > 1):
    #     return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    # else:
    #     return 'NO ISBN'