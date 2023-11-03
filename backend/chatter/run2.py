from api.answer import create_prompt_text, create_prompt_messages
from utils import kb_service as chunks
from utils import logging
import json

logger = logging.getLogger()

l = [1,2,3,4,5]
print(json.loads(l))