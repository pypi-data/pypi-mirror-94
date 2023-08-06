import logging


def stream_logger():
    # Simple logger when no provided
    logger = logging.getLogger('stream')
    logger.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    return logger
