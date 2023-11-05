from utils import logging
from db import db


logger = logging.getLogger()

def get_conversations_by_time(domain_id, start_date, end_date):
    records = db.get_conversations_by_time(domain_id, start_date, end_date)
    for record in records:
        record['date_time_started'] = record['date_time_started'].isoformat()
    return records
