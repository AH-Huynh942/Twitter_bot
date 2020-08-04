import requests
import json
# from xml.etree import ElementTree
from config import goodreads_key

import goodreads_api_client as gr

def find_purchasable_books(q):
  client = gr.Client(developer_key = goodreads_key)
  book = client.search_book('Prydain','title')
  keys_wanted = ['id', 'title', 'isbn']
  reduced_book = {k:v for k, v in book.items() if k in keys_wanted}
  print(reduced_book)


  # searchTitle = 'title'
  # url = f'https://www.goodreads.com/search.xml?key={goodreads_key}&q={q}&page={1}&search={searchTitle}'
  # response = requests.get(url)
  # tree = ElementTree.fromstring(response.content)
  # print(tree.find('search'))
  # except:
  #   pass