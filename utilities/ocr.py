import logging
logger = logging.getLogger('twitter_stream')

import requests

from config import ocr_key

# TESTING FUNCTION
def ocr_file(filename, overlay=False, api_key=ocr_key, language='eng'):
	""" OCR.space API request with local file. Python3.5 - not tested on 2.7
	:param filename: Your file path & name.
	:param overlay: Is OCR.space overlay required in your response. Defaults to False.
	:param api_key: OCR.space API key. Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
		List of available language codes can be found on https://ocr.space/OCRAPI
		Defaults to 'en'.
	:return: Result in JSON format.
	"""

	logger = logging.getLogger('TEST')

	payload = {
		'isOverlayRequired': overlay,
		'apikey': api_key,
		'scale': True,
		'OCREngine': 2, 
		'language': language,
	}
							
	with open(filename, 'rb') as f:
		r = requests.post(
			'https://api.ocr.space/parse/image',
			files={filename: f},
			data=payload,
		)

	r_json = r.json()
	logger.debug('*************************RAW JSON of OCR_FILE FUNCTION**************************')
	logger.debug(r_json)
	logger.debug('********************************************************************************')
	
	result = r_json['ParsedResults'][0]['ParsedText']

	if (result == ''):
		return False

	logger.info('**********************************OCR RAW TEXT**********************************')
	logger.info(result)
	logger.info('********************************************************************************')

	return result

# REAL FUNCTION
def find_text(url, overlay=False, api_key= ocr_key, language='eng'):
	""" OCR.space API request with remote file. Python3.5 - not tested on 2.7
	:param url: Image url.
	:param overlay: Is OCR.space overlay required in your response. Defaults to False.
	:param api_key: OCR.space API key. Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
		List of available language codes can be found on https://ocr.space/OCRAPI
		Defaults to 'en'.
	:return: Result in JSON format.
	"""

	payload = {
		'url': url,
		'isOverlayRequired': overlay,
		'scale': True,
		# 'OCREngine': 2, 
		'apikey': api_key,
		'language': language,
	}
	
	r = requests.post(
		'https://api.ocr.space/parse/image',
		data=payload,)
	
	r_json = r.json()
	logger.debug('*************************RAW JSON of OCR_FILE FUNCTION**************************')
	logger.debug(r_json)
	logger.debug('********************************************************************************')
	
	result = r_json['ParsedResults'][0]['ParsedText']

	if (result == ''):
		return False

	logger.info('**********************************OCR RAW TEXT**********************************')
	logger.info(result)
	logger.info('********************************************************************************')

	return result