import requests

# from config import google_key

def find_quote(q, maxResults = 3, projection = 'full',  ):
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
    
    # book_isbn = []
    print("**************Book Info Given***************")
    for book in results['items']:
        info = book['volumeInfo']
        # book_isbn.append(str(info['industryIdentifiers']))
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

    if (len(r.json()['items'][0]['volumeInfo']['industryIdentifiers']) > 1):
        return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    else:
        return r.json()['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
    # return book_isbn

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