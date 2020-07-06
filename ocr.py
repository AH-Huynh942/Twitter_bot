import requests

from config import ocr_key

def ocr_file(filename, overlay=False, api_key=ocr_key, language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
            #    'scale',
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    # return r.content.decode() <-- returns a string
    # return r.json() # <-- returns json
    print('********************OCR JSON***********************\n')
    print(r.json())
    print('\n')
    print('********************OCR JSON***********************\n')
    return r.json()['ParsedResults'][0]['ParsedText'] # <-- returns the interpreted string


def ocr_url(url, overlay=False, api_key= ocr_key, language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'scale': True,
            #    'OCREngine': 2, 
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    # return r.content.decode() # <-- returns entire object as string
    # return r.json() # <-- returns json
    return r.json()['ParsedResults'][0]['ParsedText'] # <-- returns the interpreted string


# Use examples:
# test_file = ocr_file(filename='test_image2.jpg', language='pol')
# test_url = ocr_url(url='http://i.imgur.com/31d5L5y.jpg')

# print(test_file['ParsedResults'][0]['ParsedText'])
# print(test_url['ParsedResults'][0]['ParsedText'])