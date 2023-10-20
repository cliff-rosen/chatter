from api.answer import create_prompt_text, create_prompt_messages
from utils import logging


logger = logging.getLogger()

res = create_prompt_text('a', 'b', 'c', [], 'e')
#print(res)

res = create_prompt_messages('instructions', 'context', 'greeting', [], 'query')
print(res)
