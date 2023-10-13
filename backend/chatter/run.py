from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from db import local_db as db

print('starting')

#step1.run()

#step2.test_chunker()
#step2.test_chunker_single_doc()
#step2.run()

step3.run()

print('done')