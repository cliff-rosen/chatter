import logging

LOG_FILENAME = 'app2.log'
LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(asctime)s  %(levelname)s - %(message)s',
                    level=LOG_LEVEL, filename=LOG_FILENAME, filemode='w')

logger = logging.getLogger('main')

def getLogger():
    return logger
