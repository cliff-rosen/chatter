from api.answer import create_prompt_text, create_prompt_messages
from utils import logging, chunks_service as chunks

logger = logging.getLogger()

res = chunks.get_chunks_from_query(1, 'hello')
print(res)
