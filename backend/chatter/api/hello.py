from utils import logging
import os
logger = logging.getLogger()


def get_hello():
    return "Hello. cwd = " + os.getcwd()