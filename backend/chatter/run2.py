from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from api.answer import create_prompt_text, create_prompt_messages
from utils import kb_service as kb, logging
from db import db
import json
import datetime

logger = logging.getLogger()


domain_id = 1
start_date = datetime.datetime(2023, 11, 1)
end_date = datetime.datetime(2024, 1, 7)

res = db.get_conversations_by_time(domain_id, start_date, end_date)
for rec in res:
    print(rec['conversation_id'], rec['date_time_started'])

