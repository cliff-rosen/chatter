from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from api.answer import create_prompt_text, create_prompt_messages
from utils import kb_service as chunks
from utils import logging
import json

logger = logging.getLogger()

step3.run()