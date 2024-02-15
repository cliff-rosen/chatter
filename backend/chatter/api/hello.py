from utils import logging, openai_wrappers as model
import os

logger = logging.getLogger()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "List 10 fruit"},
]


def get_hello():
    # return "Hello. cwd = " + os.getcwd()
    print("about to return")
    return model.generate(messages, 0.0, True)
