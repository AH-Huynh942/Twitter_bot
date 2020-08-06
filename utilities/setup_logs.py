import logging

def setup_loggers():
    '''
    For tracking problems and building statistics
    '''
    main_logger = logging.getLogger('main')
    main_logger.setLevel(logging.INFO)

    twitter_stream_logger = logging.getLogger('twitter_stream')
    twitter_stream_logger.setLevel(logging.DEBUG)

    main_file_handler = logging.FileHandler('main.log')
    twitter_stream_handler = logging.StreamHandler()

    main_formatter = logging.Formatter("%(levelname)s:%(message)s: Created at %(asctime)s")
    twitter_stream_formatter = logging.Formatter("%(message)s")
    main_file_handler.setFormatter(main_formatter)
    twitter_stream_handler.setFormatter(twitter_stream_formatter)

    main_logger.addHandler(main_file_handler)
    twitter_stream_logger.addHandler(main_file_handler)
    twitter_stream_logger.addHandler(twitter_stream_handler)
  