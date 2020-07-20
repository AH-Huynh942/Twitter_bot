# import requests
# import threading
import concurrent.futures
import httplib2

def identify_header(url): # checks amazon header for status code - 200
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228 Safari/537.36'}
  h = httplib2.Http()
  r = h.request(url, headers = headers)
  print (str(r[0]['status']) + '-- '+url)
  # return (r[0]['status'])
  return (r[0]['status'],url)

def check_urls(urls): # returns viable URLs is an array
  viable_urls = []
  with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(identify_header, url) for url in urls]

    for r in concurrent.futures.as_completed(results):
      if int(r.result()[0]) == 200:
        # viable_urls.append(str(r.result()) + " -- STATUS CODE")
        viable_urls.append(r.result()[1])
  return viable_urls
