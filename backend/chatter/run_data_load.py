from data_processor import (
    step_1_spider as step1,
    step_2_chunk as step2,
    #step_3_upsert_index as step3,
)
from utils import kb_service as kb
from db import db

from utils import openai_wrappers as model

# from utils import pinecone_wrappers as vdb, openai_wrappers as model
# from utils import utils
# import local_secrets as secrets
# emb = model.get_embedding('abc')
# print(emb)

# step1.run()
step2.run()
# step3.run()

# step1.go1()
# step2.test_chunker()
# step2.test_chunker_single_doc()

"""
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a story"},
]
print("calling")
stream = model.generate(messages, 0.0, True)
print("back")
for chunk in stream:
    print(chunk.choices[0].delta.content, end="", flush=True)

print('starting')
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]

#res = model.generate(messages, 0.0)
res = model.get_embedding('hello')
print(res)
print('done')

"""

"""
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


file = 'data_processor/sources3/Vancomycin dosing in hemodialysis patients _ DoseMe Help Center.pdf'
text = utils.read_text_from_pdf(file)
res = kb.add_document(1, 'uri', 'title', text, text)

#doc_ids = [61, 62, 63, 64, 65]
#res = kb.delete_documents(doc_ids)
#res = kb.delete_documents([67])
#res = vdb.upsert_index(**doc)
#res = vdb.index.delete([], filter = {'doc_chunk_id': 'c456'})\

##############################################

logger = logging.getLogger()

domain_id = 1
start_date = datetime.datetime(2023, 11, 1)
end_date = datetime.datetime(2024, 1, 7)

res = db.get_conversations_by_time(domain_id, start_date, end_date)
for rec in res:
    print(rec['conversation_id'], rec['date_time_started'])


'C:\\Users\\cliff\\AppData\\Local\\
    Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\
        LocalCache\\local-packages\\Python311\\site-packages\\streamlit\\__init__.py'    

CreateEmbeddingResponse(
    data=[Embedding(embedding=[-0.025058426, -0.01938856, ... -0.006119225], index=0, object='embedding')], model='text-embedding-ada-002-v2', object='list', usage=Usage(prompt_tokens=1, total_tokens=1))

"""
