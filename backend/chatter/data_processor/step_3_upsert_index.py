#import pinecone
from utils import pinecone_wrappers as vdb, openai_wrappers as model
import json
from db import db
import local_secrets as secrets

"""
TO DO:
log error if upsert response not {'upserted_count': 1}
upsert in batches

"""


'''
PINECONE_API_KEY = secrets.PINECONE_API_KEY
INDEX_NAME = "index-1"

def upsert_index(doc_id, doc_chunk_id, vector_str, domain_id):
    id_str = str(doc_chunk_id)
    vector_obj = json.loads(vector_str)
    metadata = {'domain_id': domain_id, "doc_id": doc_id, "doc_chunk_id": doc_chunk_id}
    upsert_response = index.upsert(vectors=[(id_str, vector_obj, metadata)])
    print("  response: ", upsert_response)
'''

def process_row(row):
    doc_id = row['doc_id']
    doc_chunk_id = row['doc_chunk_id']
    chunk_embedding = row['chunk_embedding']
    domain_id = row['domain_id']
    print("  Upserting: ", domain_id, doc_chunk_id, chunk_embedding[:20])
    vdb.upsert_index(doc_id, doc_chunk_id, json.loads(chunk_embedding), domain_id)

def run():
    print("Starting upsert")
    conn = db.get_connection()

    if g_domain_id == ALL_DOMAINS:
        print("Processing all domains")
        domain_recs = db.get_domains()
    else:
        print("Processing single domain", g_domain_id)
        domain_recs = [{'domain_id': g_domain_id}]
    #domain_recs = [{'domain_id': x} for x in [1] ]

    for domain_rec in domain_recs:
        domain_id = domain_rec['domain_id']
        print("--------------------------------------------")
        print("Retrieving chunks for domain ", domain_id)
        print("--------------------------------------------")
        rows = db.get_document_chunks(conn, domain_id)
        cur_count = 1
        tot_count = len(rows)
        print("Total chunks to be upserted", tot_count)
        for row in rows:
            print("Processing ", cur_count, " of ", tot_count)
            process_row(row)
            cur_count = cur_count + 1

    db.close_connection(conn)

def test():
    query = 'hello'
    query_embedding = model.get_embedding(query)
    print(vdb.get_matching_chunks(2, query_embedding))

def fetch():
    res = index.fetch(ids=['3'])
    print(res['vectors']['3']['metadata'])

# runtime settings
ALL_DOMAINS = 1000000
g_domain_id = 2

#print(index.describe_index_stats())
#run()
