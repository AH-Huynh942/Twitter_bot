import logging
logger = logging.getLogger('twitter_stream')

import concurrent.futures
import httplib2

library = httplib2.Http()

def identify_header(url): # checks amazon header for status code - 200
    '''
    Function to check individual urls for validity
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228 Safari/537.36'}
    # h = httplib2.Http() #!!! Change this to be static!
    r = library.request(url, headers = headers)
    logger.debug(f'status_code: %s, URL: {url}', r[0]['status'])
    return (r[0]['status'],url)

def check_urls(urls): # returns viable URLs is an array
    '''
    Function: check_urls - is to be imported.
    -Used to reduced lag overall.
    -Checks multiple links for viability all at once without having to constantly wait for them consecutively. 
    '''

    viable_urls = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(identify_header, url) for url in urls]

    for r in concurrent.futures.as_completed(results):
        if int(r.result()[0]) == 200:
            # viable_urls.append(str(r.result()) + " -- STATUS CODE")
            viable_urls.append(r.result()[1])
    logger.info('VIABLE_URLS--------------------------------------------------')
    logger.info(viable_urls)
    return viable_urls
