from data_processor import step_1_doc_loader as step1, step_2_chunk as step2, step_3_upsert_index as step3
from db import db

print('starting')


#step1.run()
#step1.go1()

#step2.test_chunker()
#step2.test_chunker_single_doc()
#step2.run()

#step3.run()

print('done')

import fitz
file = 'chatter/data_processor/sources2/Data States Guide.pdf'
from pypdf import PdfReader

'''
with fitz.open(file) as doc:  # open document
    #text = chr(12).join([page.get_text() for page in doc])
    text = doc[0].get_text()
print(text)
'''

reader = PdfReader(file)
print(reader.pages[0].extract_text())

'''
res = db.get_document_chunks_from_ids(['105'])
chunk = res[0]['chunk_text']
for i in range(len(chunk)):
    print(i, chunk[i], ord(chunk[i]))
'''

