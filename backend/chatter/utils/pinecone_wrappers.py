import local_secrets as secrets
from utils import logging
import pinecone
import json

PINECONE_API_KEY = secrets.PINECONE_API_KEY
INDEX_NAME = "index-1"
TOP_K = 40

logger = logging.getLogger()
logger.info('pinecone_wrapper loaded')

pinecone.init(api_key=PINECONE_API_KEY, environment="us-east1-gcp")
index = pinecone.Index(INDEX_NAME)

def upsert_index(doc_id, doc_chunk_id, vector, domain_id):
    id_str = str(doc_chunk_id)
    metadata = {'domain_id': domain_id, "doc_id": doc_id, "doc_chunk_id": doc_chunk_id}
    upsert_response = index.upsert(vectors=[(id_str, vector, metadata)])
    print("  response: ", upsert_response)

def delete_all_for_doc_id(doc_id):
    filter = {"doc_id": doc_id}
    print(filter)
    res = index.delete(filter=filter)
    return res

# retrieve TOP_K embedding matches to query embedding
# return as dict {id: {"id": id, "score": score, "metadata": metadata}}
def get_matching_chunks(domain_id, query_embedding, top_k=TOP_K):
    print("querying index")
    matches = index.query(
        top_k=top_k,
        include_values=True,
        include_metadata=True,
        vector=query_embedding,
        filter={'domain_id': domain_id}).matches
    print('  query retrieved %s results' % (len(matches)))
    if len(matches) > 0:
        res = {
                matches[i].id : {
                                "id" : int(matches[i].id),
                                "score" : matches[i].score, 
                                "metadata": matches[i].metadata
                                } for i in range(len(matches))
            }
    else:
        res = {}
    return res
