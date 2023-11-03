from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from utils import kb_service as kb
from db import db
from utils import pinecone_wrappers as vdb
from utils import utils
import local_secrets as secrets

print('starting')

#step1.run()
#step1.go1()

#step2.test_chunker()
#step2.test_chunker_single_doc()
#step2.run()

#step3.run()

import random
num_floats = 1536
vector_str = ""
for _ in range(num_floats):
    new_float = random.random()
    vector_str += str(new_float) + ", "
vector_str = '[' + vector_str[:-2] + ']'
#vector_str = '[1.0, 2.0]'
doc = {
    "doc_id": 'd123',
    "doc_chunk_id": "c456",
    "vector_str": vector_str,
    "domain_id": 99
}

'''
file = 'data_processor/sources3/Vancomycin dosing in hemodialysis patients _ DoseMe Help Center.pdf'
text = utils.read_text_from_pdf(file)
res = kb.add_document(1, 'uri', 'title', text, text)
'''

#doc_ids = [61, 62, 63, 64, 65]
#res = kb.delete_documents(doc_ids)
res = kb.delete_documents([67])

#res = vdb.upsert_index(**doc)
#res = vdb.index.delete([], filter = {'doc_chunk_id': 'c456'})\

print('res', res)


print('done')
